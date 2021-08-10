"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('schoolApp.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name = 'index'), 
    path('contact/', views.contact, name = 'contact'), 
    path('about/', views.about, name = 'about'),
    path('blog/', views.BlogListView.as_view(), name = 'blog'),
    path('blog_detail/<str:slug>/', BlogDetailView.as_view(), name = 'blog_detail'),    
    path('superuser/', views.superUserLogin, name = 'userLogin'), 
    path('logout/', views.adminLogout, name = 'logout'),
    path('superuser/dashboard', views.dashboard, name = 'dashboard'),
    path('superuser/addcategory', views.addCategory, name = 'add_category'),
    path('superuser/<str:slug>/update', views.updatePost, name='post_edit'),
    path('superuser/category', CategoryListView.as_view(), name = 'category'), 
    path('superuser/<str:slug>/edit_category', views.updateCategory, name='category_edit'),
    path('superuser/addpost', views.addPost, name = 'add_post'),
    path('superuser/posts', PostListView.as_view(), name = 'post'),
    path('superuser/<str:slug>/delete_post', views.deletePost, name='post_delete'),
    path('superuser/<str:slug>/delete_category', views.deleteCategory, name='category_delete'),   
]
