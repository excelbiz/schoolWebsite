from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, Http404, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def index(request):

    return render(request, 'index.html')

def contact(request):
    
    return render(request, 'contact.html')

def blog(request):
    
    return render(request, 'blog.html')

def about(request):
    
    return render(request, 'about.html')

@login_required(login_url= 'userLogin')
def dashboard(request):
    
    return render(request, 'Admin/dashboard.html')

def superUserLogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        admin = authenticate(request, username = username, password = password)

        if admin is not None:
            login(request, admin)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid Login Details')
            return redirect('userLogin')
    
    return render(request, 'Admin/login.html')

@login_required(login_url= 'userLogin')
def addPost(request):
    form = postForm()
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            blog_title = form.cleaned_data.get('title')
            form.save()
            messages.success(request, blog_title + ' was posted successfully!')
            return redirect('post')
    else:
        form = postForm()
    return render(request, 'Admin/addPost.html', {'form':form})

@login_required(login_url= 'userLogin')
def addCategory(request):
    form = categoryForm()
    if request.method == 'POST':
        form = categoryForm(request.POST or None)
        if form.is_valid():
            cat = form.cleaned_data.get('name')
            form.save()
            messages.success(request, cat + ' was added successfully!')
            return redirect('view_category')
    else:
        form = categoryForm()
    return render(request, 'Admin/addCategory.html', {'form':form})


def adminLogout(request):
    logout(request)
    return redirect('userLogin')

class PostListView(ListView):
    template_name = 'Admin/view_post.html'
    context_object_name = 'posts'
    ordering = ['-published_at']
    paginate_by = '10'

    def get_queryset(self):
        post = Post.objects.all()
        return post

class BlogListView(ListView):
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-published_at']
    paginate_by = '10'

    def get_queryset(self):
        post = Post.objects.all()
        return post

class CategoryListView(ListView):
    template_name = 'Admin/view_category.html'
    context_object_name = 'categories'
    ordering = ['-published_at']
    paginate_by = '10'

    def get_queryset(self):
        category = Category.objects.all()
        return category

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()[:10]
    #     context['latest_posts'] = Post.objects.all()[:5]
    #     context['num_categories'] = Post.objects.count()
    #     return context
    

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'single-blog.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_post'] = Post.objects.all()[:5]
#         context['categories'] = Category.objects.all()[:10]
#         return context
