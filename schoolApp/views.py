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
def updatePost(request, slug):
    post = Post.objects.get(slug = slug)
    form = postForm(request.POST or None, request.FILES or None, instance = post)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        form.save()
        messages.success(request, title + ' Updated Successfully!')
        return redirect('post')
    return render(request, 'Admin/update_post.html', {'form':form})

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


@login_required(login_url= 'userLogin')
def updateCategory(request, slug):
    cat = Category.objects.get(slug = slug)
    form = categoryForm(request.POST or None, instance = cat)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        form.save()
        messages.success(request, name + ' Updated Successfully!')
        return redirect('view_category')
    return render(request, 'Admin/update_category.html', {'form':form})

@login_required(login_url= 'userLogin')
def deletePost(request, slug):
    post = Post.objects.get(slug = slug)
    if request.method == 'POST':
        post.delete()
        messages.info(request, 'Blog Post Deleted Successfully!')
        return redirect('post')
        
    context = {
        'post': post
    }

    return render(request, 'Admin/delete_post.html', context)


@login_required(login_url= 'userLogin')
def deleteCategory(request, slug):
    category = Category.objects.get(slug = slug)
    if request.method == 'POST':
        category.delete()
        messages.info(request, 'Category Deleted Successfully!')
        return redirect('view_category')
        
    context = {
        'category': category
    }

    return render(request, 'Admin/delete_category.html', context)


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
    paginate_by = '2'

    def get_queryset(self):
        post = Post.objects.all()
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_post'] = Post.objects.all()[:5]
        return context

class CategoryListView(ListView):
    template_name = 'Admin/view_category.html'
    context_object_name = 'categories'
    ordering = ['-published_at']
    paginate_by = '10'

    def get_queryset(self):
        category = Category.objects.all()
        return category

def searchBlog(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        result = Post.objects.filter(title__contains=search)
        category = Category.objects.all()
        posts = Post.objects.all().order_by('-published_at')[:2]

        return render(request, 'search_result.html', {'result': result, 'query': request.POST, 'category':category, 'posts':posts})    

def visitorLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        visitor = authenticate(request, username = username, password = password)

        if visitor is not None:
            login(request, visitor)
            return redirect('blog')
        else:
            messages.warning(request, 'Invalid Login Details')
            return redirect('login')
    return render(request, 'login.html')

def VisitorLogout(request):
    logout(request)
    return redirect('index')


def visitorReg(request):
    form = VisitorForm()
    post = Post.objects.all()[:3]
    if request.method == 'POST':
        form = VisitorForm(request.POST or None)
        if form.is_valid():
            visitor = form.cleaned_data.get('username')
            visit_obj = form.save(commit = False)
            visit_obj.user = User.objects.create_user(

                password = form.cleaned_data.get('password2'),
                username = form.cleaned_data.get('username'),
            )
            visit_obj.save()
            messages.success(request, 'Account for ' + visitor + ' was created successfully!')
            return redirect('index')

    else:
        form = VisitorForm()
    return render(request, 'register.html', {'form':form, 'posts':post})


def blogDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    query = Comment.objects.filter(post=post)
    form = commentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit = False)
        comment.commenter = request.user
        comment.post = post
        comment.save()
        messages.success(request, "You Commented on this post!")
        return redirect('blog_detail', slug = post.slug)
    latest_post = Post.objects.all()[:3]
    post.noOfViews = post.noOfViews + 1
    post.save()
    return render(request, 'single_blog.html', {'posts': post, 'latest_post':latest_post, 'replies' : query, 'form':form})
