from django.urls import path
from django.views.static import serve
from django.conf import settings
from . import views


urlpatterns = [
    path('create/', views.create_new_blog, name='create_blog'),
    path('my-blogs/<str:username>/', views.user_blogs, name='user_blogs'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('blog/<int:blog_id>/like_dislike/', views.like_dislike_blog, name='like_dislike_blog'),
    path('comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('all_comments/', views.user_comments, name='user_comments'),
] 