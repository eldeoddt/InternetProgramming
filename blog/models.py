from django.db import models
from django.contrib.auth.models import User
import os

# Tag 모델 만들기
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # tag 클릭 시 blog/tag/태그명/ return한다.
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

# SlugField 만들기 : 숫자pk 대신 텍스트로 url을 만들 때 사용한다.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # url을 읽을 수 있게 된다.
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

class Post(models.Model):
    #charfield: 한 줄만 입력
    #textfield: 텍스트 폼 여러 줄 입력


    # 이미지가 년도, 월, 일 순서로 저장된다.
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)

    # 파일 필드 지정
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    #db cloumn을 생성하는데, model -> title을 넣어주겠다.
    title = models.CharField(max_length=30)
    #db cloumn을 생성하는데, model -> content를 넣어주겠다.
    content = models.TextField()

    # db cloumn을 생성하는데, model -> 시간정보를 넣어주겠다.
    # 현재 시간을 새로 작성할 때 바로 넣게 한다.
    created_at = models.DateTimeField(auto_now_add=True)

    #update_at 테이블 새로 생성된다 -> migration 반복작업 다시 해야 한다.
    # 수정 시간을 업데이트 했을 때, 수정 시간을 현재 시간으로 교체
    update_at = models.DateTimeField(auto_now = True)

    #author: 글쓴이 저장 객체 생성
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    #category 객체 생성. blank=True 로 카테고리 미지정 가능하게 한다.
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)

    # tag 필드 추가. 다대다 관계
    # 클래스명, null=True를 설정할 필요 없다. 공란만 허용하면 된다.
    tags = models.ManyToManyField(Tag, blank=True)

    #str함수 정의하여 post의 제목을 보이게 하기
        #self가 가지고 있는 프라이머리키, self가지고 있는 title을 return해주겠다는 의미이다.
        #문자열을 반환할 때 f를 사용하는데, {}를 사용하면 실제 값에 접근하여 문자열로 변환한다는 의미이다.
        # [1]첫번째 포스트입니다 로 출력되게 한다.
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    # post마다 고유 url 부여하기.
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'