# -*- coding: utf-8 -*-

from django import forms
from .models import Catalog, ExpresFiles, Files

class CatalogForms(forms.ModelForm):
    cover = forms.ImageField()
    title = forms.CharField()
    category = forms.ModelChoiceField(
        queryset=None,
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

class ExpresFilesForms(forms.ModelForm):
    email = forms.EmailField()
    description = forms.Textarea()

    class Meta:
        model =ExpresFiles
        fields=['email', 'description']

class FilesForms(forms.ModelForm):
    catalog = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select()
    )
    expresfile = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select()
    )
    files_s = forms.FileField()

    class Meta:
        model=Files
        fields=['catalog', 'expresfile', 'files_s']
