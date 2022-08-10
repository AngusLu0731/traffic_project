from django.db.models.aggregates import Count
from .models import Stream
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm): #註冊表單
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'--註冊後不能改--'})
    )
    first_name= forms.CharField(
        label="暱稱",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'--簡單稱號--'})
    )
    email = forms.EmailField(
        label="電郵",
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'--你的E-Mail--'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'--不要太短--'})
    )
    password2 = forms.CharField(
        label="確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'--密碼確認--'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name',]



class LoginForm(forms.Form): #登入表單
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'--沒有請註冊--'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'--沒有請註冊--'})
    )

class FeedBackForm(forms.ModelForm): #回饋表單
    message = forms.CharField(label="",widget=forms.Textarea)
    class Meta:
        model = Stream
        fields = ['message',]