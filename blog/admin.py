from django.contrib import admin
from blog.models import Post, Category, Tag

#Post 모델 admin에 등록하기
admin.site.register(Post)


# SlugField 자동으로 생성하는 admin 기능 만들기
class CategoryAdmin(admin.ModelAdmin):
    #prepopulated_fields : name 필드값으로 slug를 자동 생성하도록 설정한다.
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)

# Tag 생성하는 admin 기능 만들기. from models import Tags 해야 한다.
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Tag, TagAdmin)