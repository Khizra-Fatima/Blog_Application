from django.urls import path
from . import views

urlpatterns = [
    path('bookmark/<int:blog_id>/', views.bookmark_blog, name='bookmark_blog'),
    path('bookmarked-blogs/', views.bookmarked_blog, name='bookmarked_blog'),
    path('delete-bookmark/<int:bookmark_id>/', views.delete_bookmark_blog, name='delete_bookmark_blog'),
    path('delete-all-bookmarks/', views.clear_bookmark, name='clear_bookmark'),
]
