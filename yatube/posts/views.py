from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm

from .models import Group, Post, User

from .utils import paginator_func


def index(request):
    post_list = Post.objects.select_related('author', 'group').all()
    context = {
        'page_obj': paginator_func(post_list, request),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_list = group.posts.select_related('author').all()
    context = {
        'group': group,
        'page_obj': paginator_func(group_list, request),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.select_related('group').all()
    context = {
        'author': author,
        'page_obj': paginator_func(author_posts, request),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', post.author.username)
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('posts:post_detail', post.pk)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)
