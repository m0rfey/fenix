# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory

from .models import Category, Catalog, ExpresFiles, FilesCatalog, FilesExpres

class CatalogForms(forms.ModelForm):
    cover = forms.ImageField()
    title = forms.CharField()
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select()
    )
    description = forms.Textarea()
    is_open = forms.BooleanField(widget=forms.CheckboxInput())
    is_slug = forms.BooleanField(widget=forms.CheckboxInput())
    is_for_me = forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model = Catalog
        fields = ['title',
                  'cover',
                  'category',
                  'description',
                  'is_open',
                  'is_slug',
                  'is_for_me']

class FilesExpresForms(forms.ModelForm):
    files_s = forms.FileField(
        label='Файл',
        required=False,
        widget= forms.FileInput())
    class Meta:
        model=FilesExpres
        fields=['files_s']

class ExpresFilesForms(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput({'class': 'form-control','placeholder': 'Email'})
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea({'class': 'form-control','placeholder': 'Описание'}))

    class Meta:
        model=ExpresFiles
        fields=['email', 'description']

class TestForm(ExpresFilesForms, FilesExpresForms):
    inlineformset_factory = ['email', 'description', 'files_s']

class SearchForm(forms.Form):
    search = forms.CharField(
        label='',
        widget=forms.TextInput({'class':'form-control', 'placeholder':'Поиск'})
    )
    field = ['search']

class SearchKey(forms.Form):
    s_key = forms.CharField(
        label='',
        widget=forms.TextInput({'class':'form-control', 'placeholder':'Введите ключ'})
    )
    field = ['s_key']
