from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('store', views.store, name='store'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]