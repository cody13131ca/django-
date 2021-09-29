from django.shortcuts import resolve_url, redirect, render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category, DisLike
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm, SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from taggit.models import Tag
from django.db.models import Count
# from django.core.paginator import Paginator


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        return post.author == self.request.user


class Index(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context


class Indexlike(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-like')
        context = {
            'post_list': post_list,
        }
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

        def get_success_url(self):
            messages.success(self.request, 'Postを登録しました。')
            return resolve_url('myapp:index')


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        detail_data = Post.objects.get(id=self.kwargs['pk'])
        category_posts = Post.objects.filter(
            category=detail_data.category).order_by('-created_at')
        related_items = self.object.tags.similar_objects()

        params = {
            'object': detail_data,
            'category_posts': category_posts,
            'related_items': related_items,
        }
        return params


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, 'Postを更新しました。')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])


class PostDelete(OnlyMyPostMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.warning(self.request, 'Postを削除しました。')
        return resolve_url('myapp:index')


class PostList(ListView):
    paginate_by = 10
    model = Post

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'


class Logout(LogoutView):
    template_name = 'myapp/logout.html'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.success(self.request, 'ユーザー登録をしました。')
        return HttpResponseRedirect(self.get_success_url())


@login_required
def Like_add(request, post_id):
    post = Post.objects.get(id=post_id)

    is_liked = Like.objects.filter(user=request.user, post=post_id).count()
    like = Like()
    url = request.META.get('HTTP_REFERER')

    if is_liked > 0:
        messages.info(request, 'いいねを取り消しました。')
        Like.objects.filter(user=request.user, post=post_id).delete()
        return redirect(url)

    else:
        like.user = request.user
        like.post = post
        like.save()

        messages.success(request, '投稿にいいねしました！')
        return redirect(url)


@login_required
def DisLike_add(request, post_id):
    post = Post.objects.get(id=post_id)
    dislike = DisLike()
    is_disliked = DisLike.objects.filter(
        user=request.user, post=post_id).count()
    url = request.META.get('HTTP_REFERER')

    if is_disliked > 0:
        messages.info(request, 'よくないねを取り消しました。')
        DisLike.objects.filter(user=request.user, post=post_id).delete()
        return redirect(url)

    else:
        dislike.user = request.user
        dislike.post = post
        dislike.save()

        messages.warning(request, 'よくないねしました。')
        return redirect(url)


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(name_en=self.kwargs['name_en'])
        category_posts = Post.objects.filter(
            category=detail_data.id).order_by('-created_at')

        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }

        return params


class TagList(ListView):
    model = Tag


class TagDetail(DetailView):
    model = Tag

    def get_context_data(self, *args, **kwargs):
        tag_lists = Tag.objects.all().annotate(blog_count=Count(
            'taggit_taggeditem_items')).order_by('-blog_count')

        params = {
            'tag_lists': tag_lists
        }
        return params


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Post.objects.filter(Q(title__icontains=freeword) | Q(
                content__icontains=freeword) | Q(
                author__username__icontains=freeword) | Q(
                    category__name__icontains=freeword) | Q(
                        tags__name__icontains=freeword)).distinct()

        params = {
            'search_list': search_list,
        }

        return render(request, 'myapp/search.html', params)


# Create your views here.
