from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


from utils.models import TimeStampedModel

User = get_user_model()

# 블로그에 필요한 것들?
# 1. 제목
# 2. 본문
# 3. 글쓴이 => 추후 업데이트
# 4. 작성일자
# 5. 수정일자
# 6. 카테고리
# 썸네일이미지, 태그

class Blog(TimeStampedModel):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel','여행'),
        ('cat','고양이'),
        ('dog','강아지'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목',max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 ( 유저를 삭제하려고 할때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => 유저 삭제시 블로그의 author가 NULL이 됩니다. 예시) on_delete=models.SET_NULL, null=True 이렇게 null값을 true로 넣어야 함

    image = models.ImageField('이미지',  null=True, blank=True, upload_to='blog/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='blog/%Y/%m/%d/thumbnail')
    # ImageField를 사용할려면 pillow라는 라이브러리가 필요함 -> poetry add pillow
    # 2026/02/04
    # blog/2024/02/04 이미지파일.jpg
    # ImageField, Field와 같지만 이미지만 업로드하게 되어있다.
    # 보통 varchar로 되어 있는데 경로만 저장하기 때문이다.


    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}]'
                  # get_category_display() choices=CATEGORY_CHOICES 이처럼 choices쓴거에만 사용 가능
                  # get_컬럼명_display() 이러면 저 위에 앞에 free가 아닌 자유가 화면에 보임
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk': self.pk})

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300,300))

        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem # blog/2026/02/05/database.png => database
        thumbnail_extension = image_path.suffix.lower() # blog/2026/02/05/database.png => .png
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}' # database_thumb.png

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_name, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

    # category update (terminal)
    # BLog.objects.filter(category='').update(category='free')

    # 댓글기능
    # blog 정보 (게시글)
    # 댓글 내용
    # 작성자
    # 작성일자
    # 수정일자
class Comment(TimeStampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'

