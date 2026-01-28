from django.db import models

# 블로그에 필요한 것들?
# 1. 제목
# 2. 본문
# 3. 글쓴이 => 추후 업데이트
# 4. 작성일자
# 5. 수정일자
# 6. 카테고리
# 썸네일이미지, 태그

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel','여행'),
        ('cat','고양이'),
        ('dog','강아지'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('제목',max_length=100)
    content = models.TextField('본문')

    created_at=models.DateTimeField('생성일자',auto_now_add=True)
    updated_at=models.DateTimeField('수정일자',auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}]'
                  # get_category_display() choices=CATEGORY_CHOICES 이처럼 choices쓴거에만 사용 가능
                  # get_컬럼명_display() 이러면 저 위에 앞에 free가 아닌 자유가 화면에 보임
    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

