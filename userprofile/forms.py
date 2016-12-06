# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from userprofile.models import User


class SignUpForm(UserCreationForm):
    username= forms.CharField(
        label='',
        max_length=50,
        required=True,
        widget=forms.TextInput({'class': 'form-control','placeholder': 'Логин'})
    )
    email = forms.EmailField(
        label='',
        max_length=50,
        required=True,
        widget=forms.TextInput({'class': 'form-control','placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label='',
        max_length=50,
        required=True,
        widget=forms.PasswordInput({'class': 'form-control','placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='',
        max_length=50,
        required=True,
        widget=forms.PasswordInput({'class': 'form-control','placeholder': 'Подтверждение пароля'})
    )

    class Meta:
        model =User
        fields = ['username', 'email', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    username= forms.CharField(
        label='',
        max_length=50,
        required=True,
        widget=forms.TextInput({'class': 'form-control','name': 'username','placeholder': 'Логин'})
    )
    password = forms.CharField(
        label='',
        max_length=50,
        required=True,
        widget=forms.PasswordInput({'class': 'form-control', 'name': 'password', 'placeholder': 'Пароль'})
    )
    class Meta:
        model = User
        filter =['username', 'password']
