from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # 로그인한 방문자만 접근 가능하도록 한다. 접근 가능영역 설정
from django.core.exceptions import PermissionDenied # 접근 권한이 있는 방문자인지 확인한다.


# form view 생성
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post # post 모델을 그대로 사용한다는 의미이다.
    # 사용자들에게 입력받을 필드를 array 형식으로 설정한다.
    # 반드시! 필드들은 post에 정의되어 있는 column이어야 한다.
    # created_at 등 autor 등은 현재 로그인된 정보를 바탕으로 사용하기 때문에 따로 지정하지 않는다.
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # UserPassesTestMixin 에서 확인할 조건. 최고권한 또는 스태프인 경우
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # form_valid() redirect import 가 필요하다.
    # author 필드를 자동으로 채우기 위해 CreateView에서 제공하는 form_valid 사용한다.
    # self.request.user : 웹 사이트 방문자
    # is_authenticated : 로그인 되었는지 확인
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


# 존재하는 레코드를 수정하는 페이지 만들 때 PostUpdate 사용.
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        # 권한을 갖고 있고 and 게시물 author인지 ?
        if request.user.is_authenticated and request.user == self.get_object().author:
            # post를 update한다.
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied # 아닌 경우 403에러 발생.

# 삭제 구현
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/blog' # 게시글 지우고 난 후 어디를 보여줄 것인지 지정한다.

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # post를 delete한다.
            return super(PostDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied # 아닌 경우 403에러 발생.



# urls.py에서 호출할 tag_page 구현
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(request, 'blog/post_list.html',
{
        'post_list' : post_list,
        'tag' : tag,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count()
        }
    )

def category_page(request, slug):
    # 카테고리 있는 경우, 없는 경우 분류하여 처리하기
    if slug == 'no_categories':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    # 카테고리가 있을 때는 slug로 반환한다.
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_categories_post_count' : Post.objects.filter(category=None).count(),
            'category' : category,
        }
    )
class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        #Post.objects.all() 과 달리 category=None인 Post만 보여준다.
        context['no_categories_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        # 모든 카테고리 객체를 가져옴.
        context['categories'] = Category.objects.all()
        # 미분류
        #Post.objects.all() 과 달리 category=None인 Post만 보여준다.
        context['no_categories_post_count'] = Post.objects.filter(category=None).count()
        return context

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