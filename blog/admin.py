from django.contrib import admin
from blog.models import Post

#Post 모델 admin에 등록하기
admin.site.register(Post)