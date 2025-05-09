from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/edit/<int:user_id>', views.edit_profile, name='edit_profile'),
]