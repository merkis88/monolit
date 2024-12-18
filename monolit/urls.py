from tkinter.font import names
from venv import create

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('deleteaccount/', views.delete_account, name="delete_account"),
    path('create/', views.create_post, name="create_post"),
    path('post/<int:post_id>/', views.post_detail, name="post_detail"),
    path('vote/<int:post_id>/', views.vote_post, name='vote_post'),
    path('posts/', views.post_list, name="post_list"),

]