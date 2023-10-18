from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post
    ordering = '-pk'
class PostDetail(DetailView):
    model = Post

#FBV 방식으로 코딩함.

# def index(request):
#     #order_by('-pk') : pk 역순으로 나열한다는 의미이다.
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts' : posts,
#         }
#     )