#  yatube_project/yatube/posts/views.py
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def authorized_only(func):
    # Функция-обёртка в декораторе может быть названа как угодно
    def check_user(request, *args, **kwargs):
        # В любую view-функции первым аргументом передаётся объект request,
        # в котором есть булева переменная is_authenticated,
        # определяющая, авторизован ли пользователь.
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')

    return check_user


QUANT_OF_POSTS: int = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    # убрал_.order_by('-pub_date')_
    paginator = Paginator(posts, QUANT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # 'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all().filter(group=group)
    paginator = Paginator(posts, QUANT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Здесь код запроса к модели и создание словаря контекста
def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, QUANT_OF_POSTS)
    template = 'posts/profile.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    detail_post = get_object_or_404(Post, id=post_id)
    post_count = Post.objects.filter(author=detail_post.author).count()
    template = 'posts/post_detail.html'
    context = {
        'post_count': post_count,
        'detail_post': detail_post,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.text = form.cleaned_data['text']
        post.author = request.user
        form.save()
        return redirect('posts:profile', username=request.user)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'post_id': post_id,
        'post': post,
        'is_edit': is_edit,
    }
    return render(request, 'posts/create_post.html', context)
