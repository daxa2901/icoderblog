from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('postComment', views.postComment , name='postComment'),
    path('signup', views.handleSignup, name='signup'),
    path('login', views.handleLogin, name='login'),
    path('logout', views.handleLogout, name='logout'),
    path('<str:slug>', views.blogPost , name='blogPost'),
   
    
]
