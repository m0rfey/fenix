# -*- coding: utf-8 -*-
from django.contrib import auth
from django.http import Http404
from django.shortcuts import render
from .models import Category, Catalog, Files

def index(request):
    args={}
    args['title'] = 'Home'
    args['catalog'] = Catalog.objects.filter(is_open=True)
    args['verbose_name'] = Category._meta.verbose_name
    args['username'] = auth.get_user(request).username
    return render(request, '../templates/catalog/index.html', args)

def category(request, category_slug):
    args={}
    args['username'] = auth.get_user(request).username
    try:
        args['title'] = Category.objects.get(slug = category_slug)
        args['category'] = Catalog.objects.filter(category=Category.objects.get(slug=category_slug), is_open=True)
    except Category.DoesNotExist:
        raise Http404
    return render(request, '../templates/catalog/category.html', args)

def view_details(request, file_id):
    args={}
    try:
        args['username'] = auth.get_user(request).username
        args['title']=Catalog.objects.filter(id=file_id).values('title')
        args['catalog']= Catalog.objects.filter(id=file_id, is_open=True)
        args['files'] = Files.objects.filter(catalog=file_id)
    except Catalog.DoesNotExist:
        raise Http404
    return render(request, '../templates/catalog/view_details.html', args)
