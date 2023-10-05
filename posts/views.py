from comments.forms import CommentForm
from comments.models import Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


@login_required
def index(request):
  posts = Post.objects.all()
  return render(request, 'posts/index.html', context={'posts': posts})


@login_required
def store(request):
  form = PostForm(request.POST or None)
  if request.POST:
    if form.is_valid():
      try:
        form.instance.user = request.user
        form.save()
        messages.success(request, 'success create post')
        return redirect('posts:index')  
      except ValidationError as e:
        form.add_error(e)
        messages.warning(request, 'validation error occurred')
  return render(request, 'posts/store.html', context={'form': form})

@login_required
def show(request, id):
  post = get_object_or_404(Post, id=id)
  if post.user.id != request.user.id:
    raise Http404
  form = CommentForm()
  comments = Comment.objects.get_comments_for_post(post.id)
  return render(request, 'posts/show.html', context={'post': post, 'comment_store_form': form, 'comments': comments})


@login_required
def update(request, id):
  post = get_object_or_404(Post, id=id)
  if post.user.id != request.user.id:
    raise Http404
  form = PostForm(request.POST or None , instance=post)
  if form.is_valid():
    form.save()
    messages.success(request, 'success update post')
    return redirect('posts:index') 
  return render(request, 'posts/update.html', context={'form': form})


@login_required
def delete(request, id):
  post = get_object_or_404(Post, id=id)
  if post.user.id != request.user.id:
    raise Http404
  post.delete()
  messages.success(request, 'success delete post')
  return redirect('posts:index')