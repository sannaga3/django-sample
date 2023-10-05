from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_update', views.user_update, name='user_update'),
    path('password_update', views.password_update, name='password_update'),
]


