from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 150)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to = 'postImages', blank = True, null = True)
    category = models.ManyToManyField('Category', help_text = 'select a category for this post' )
    slug = models.SlugField(null = True, blank = True)
    published_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
            if self.slug is None and self.title:
                self.slug = slugify(str(self.title))
            return super(Post, self).save(*args, **kwargs)

    def display_category(self):
        return ', '.join(category.name for category in self.category.all()[:3])
    
    display_category.short_description = 'Categories'
    

class Category(models.Model):
    name = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class Course(models.Model):
    title = models.CharField(max_length = 255)
    course_price = models.PositiveIntegerField(default = 0)
    content = models.TextField()
    image = models.ImageField(upload_to = 'courseImages')
    category = models.CharField(max_length = 100)
    slug = models.SlugField(null = True, blank = True)
    uploaded_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
            if self.slug is None and self.title:
                self.slug = slugify(str(self.title))
            return super(Course, self).save(*args, **kwargs)

        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    commenter = models.ForeignKey('Visitor', on_delete = models.CASCADE)
    comment = models.TextField()
    date_created = models.DateField(auto_now_add = True)
    time_created = models.TimeField(auto_now_add = True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.commenter.username.capitalize())
    

class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email = models.EmailField()
    date_joined = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.user
    

    