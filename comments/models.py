from django.db import models
from users.models import BaseMeta


class CommentManager(models.Manager):
    def get_comments_for_post(self, post_id):
        return self.filter(post_id=post_id).order_by('-id').all()


class Comment(BaseMeta):
  content = models.TextField(max_length=100)
  user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
  post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
  objects = CommentManager()
  
  class Meta:
    db_table = 'comments'

  def __str__(self):
    return self.content
