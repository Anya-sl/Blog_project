from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def padjinator(request, post_list):
    """Разбить посты постранично по 10 шт."""
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Вернуть рендер главной страницы."""
    post_list = Post.objects.select_related('author', 'group').all()
    page_obj = padjinator(request, post_list)
    context = {'page_obj': page_obj, }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Вернуть рендер страницы сообщества."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author').all()
    page_obj = padjinator(request, post_list)
    context = {'group': group,
               'page_obj': page_obj,
               }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Вернуть рендер страницы пользователя."""
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related(
        'author', 'group').filter(author=author)
    page_obj = padjinator(request, post_list)
    posts_count = post_list.count()
    context = {'author': author,
               'page_obj': page_obj,
               'posts_count': posts_count,
               }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Вернуть рендер страницы с постом."""
    post = get_object_or_404(Post, id=post_id)
    posts_count = Post.objects.select_related(
        'author', 'group').filter(author=post.author).count()
    context = {'post': post,
               'posts_count': posts_count,
               }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Создать новый пост пользователя."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
    else:
        form = PostForm()
    context = {'form': form,
               }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """Редактировать пост пользователя."""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post.id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form,
               'is_edit': True
               }
    return render(request, 'posts/create_post.html', context)
