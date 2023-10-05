from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from posts.models import Post

from .forms import CommentForm
from .models import Comment


@login_required
def store(request):
  form = CommentForm(request.POST or None)
  post = get_object_or_404(Post, id=request.POST.get('post_id'))
  if post.user.id != request.user.id:
    raise Http404
  if request.POST:
    if form.is_valid():
      try:
        form.instance.user = request.user
        form.instance.post = post
        form.save()
        messages.success(request, 'success create post')
      except ValidationError as e:
        form.add_error(e)
        messages.warning(request, 'validation error occurred')
  return redirect('posts:show', post.id)


@login_required
def update(request, id):
  comment = get_object_or_404(Comment, id=id)
  if comment.user.id != request.user.id:
    raise Http404
  form = CommentForm(request.POST or None , instance=comment)
  if form.is_valid():
    form.save()
    messages.success(request, 'success update post')
    return redirect('posts:show', comment.post_id)
  return render(request, 'comments/update.html', context={'form': form })


@login_required
def delete(request, id):
  comment = get_object_or_404(Comment, id=id)
  post_id = comment.post_id
  if comment.user.id != request.user.id:
    raise Http404
  comment.delete()
  messages.success(request, 'success delete comment')
  return redirect('posts:show', post_id)

