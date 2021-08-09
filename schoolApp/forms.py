from django import forms
from django.db.models import fields
from .models import *

class postForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(postForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(categoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'