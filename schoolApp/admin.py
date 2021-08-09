from django.contrib import admin
from .models import *

# Register your models here.



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'display_category')
    ordering = ['-id']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ['-id']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment', 'date_created')
    ordering = ['-id']

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'date_joined')
    ordering = ['-id']

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'course_price')
    ordering = ['-id']
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Course, CourseAdmin)
