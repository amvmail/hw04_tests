#  yatube_project/yatube/posts/urls.py
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    # начальная страница
    path('', views.index, name='posts'),
    # посты групп
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    # профайл user
    path('profile/<str:username>/', views.profile, name='profile'),
    # просмотр записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # создание нового поста
    path('create/', views.post_create, name='post_create'),
    # редактирование поста
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]
