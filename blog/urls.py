from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/' , views.PostDetail.as_view()),
    path('', views.PostList.as_view()),

    # update url 추가
    path('update_post/<int:pk>', views.PostUpdate.as_view()),

    # delete url 추가
    path('delete_post/<int:pk>', views.PostDelete.as_view()),

    #category_page를 만들어서 fbv방식으로 반환하겠다는 의미이다. 쉼표에 주의한다.
    path('category/<str:slug>/',views.category_page),

    # tag를 눌렀을 때, /blog/tag/slug, tag_page의 함수의 데이터를 집어 넣어서 return해줄 것이다.
    path('tag/<str:slug>/', views.tag_page),

    # form url post 생성하는 url이다.
    path('create_post/', views.PostCreate.as_view()),

    #path('<int:pk>/', views.single_post_page),
    #path('', views.index),
]
