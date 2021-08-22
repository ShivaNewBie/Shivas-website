from django.forms import ModelForm
from django import forms

from .models import Product, Comment

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['prodname', 'description','price','image']



class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    # password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a password', }))
    # password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('description', )
