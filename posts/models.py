from django.db import models
from users.models import BaseMeta


class Post(BaseMeta):
  title = models.CharField(max_length=30)
  content = models.TextField(max_length=200)
  user = models.ForeignKey('users.User', on_delete=models.CASCADE)
  
  class Meta:
    db_table = 'posts'

  def __str__(self):
    return self.title