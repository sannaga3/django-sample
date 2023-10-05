from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class BaseMeta(models.Model):
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = models.DateTimeField(default=timezone.now)
  class Meta:
    abstract = True

class UserManager(BaseUserManager):
  def create_user(self, username, email, password):
    if not email:
      raise ValidationError('Email required!')
    user = self.model(username=username, email=email)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, username, email, password):
    user = self.model(username=username, email=email)
    user.set_password(password)
    user.is_staff = True
    user.is_active = True
    user.is_superuser = True
    user.save(using=self._db)
    


class User(AbstractBaseUser, PermissionsMixin, BaseMeta):
  username = models.CharField(max_length=20)
  email = models.EmailField(max_length=50, unique=True)
  age = models.PositiveIntegerField(blank=True, null=True)
  is_active = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  
  objects = UserManager()
  
  class Meta:
    db_table = 'users'
  
  def __str__(self):
    return self.email
  
  from django.contrib.auth.models import User

from django.db import models


class Profile(BaseMeta):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  picture = models.FileField(null=True, blank=True, upload_to='picture/')
  
  class Meta:
    db_table = 'profiles'
    

