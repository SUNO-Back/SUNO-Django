from django.db import models

# Create your models here.

# Model = DB의 테이블
# Field = DB의 컬럼

# 북마크
# 이름 => varchar Django에서는 CharField라고 사용한다.
# URL주소 => varchar으로 많이 쓰지만 Django에는 URLField라는게 존재함.

class Bookmark(models.Model):
    name = models.CharField('이름',max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시',auto_now_add=True)
    updated_at = models.DateTimeField('수정일시',auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'

# makemigrations => migration.py 파일을 만든다.
# 실제 DB에는 영향 X 실제 DB에 넣기위한 정의를 하는 파일을 생성

# migrate -> migrations/ 폴더 안에 있는 migration 파일들을 실제 DB에 적용을 합니다.

# makemigrations => git의 commit이라고 보면 된다. git에 올라가지는 않는것 처럼. => DB에 적용 X, 적용할 파일 생성
# migrate => git의 push라고 보면 된다. 로컬에 있는 커밋 기록 => DB에 적용된다. migrations 파일 기록을 가지고 적용한다.
