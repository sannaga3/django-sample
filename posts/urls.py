from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('index', views.index, name='index'),
    path('store', views.store, name='store'),
    path('show/<int:id>', views.show, name='show'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]