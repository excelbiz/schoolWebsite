from django import forms
from django.db.models import fields
from .models import *
from django.core.exceptions import ObjectDoesNotExist

class postForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(postForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(commentForm, self).__init__(*args, **kwargs)
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

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ['user']

    email = forms.EmailField(
        widget = forms.EmailInput(attrs = {'placeholder': 'Email', 'class': 'form-control form-control-lg'})
    )
    
    username = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'Username', 'class': 'form-control form-control-lg'})
    )
    

    password1 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'placeholder': 'Password', 'class': 'form-control form-control-lg'}),
        min_length = 8
     )
        
    password2 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password', 'class': 'form-control form-control-lg'}),
        min_length = 8   
    )
        
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords Do not Match')
        
        
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email Already Exist')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('The User Name already exits')