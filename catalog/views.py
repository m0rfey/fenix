# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from catalog.forms import ExpresFilesForms, FilesExpresForms, TestForm
from fenix import settings
from .models import Category, Catalog, FilesCatalog, FilesExpres, ExpresFiles

from formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import UserManager

def index(request):
    args={}
    args['title'] = 'Home'
    args['catalog'] = Catalog.objects.filter(is_open=True, category__is_publish=True)
    args['expres_form'] = TestForm()
    args['username'] = auth.get_user(request).username
    return render(request, '../templates/catalog/index.html', args)

def expres_save(request):
    args={}
    args['username'] = auth.get_user(request).username
    args['expres_form'] = TestForm()
    if request.POST:
        ema =request.POST.get('email','')
        desc= request.POST.get('description', '')
        f = request.FILES.get('files_s', '')
        form = TestForm(request.POST, request.FILES)
        random_slug = UserManager().make_random_password(length=25)
        if form.is_valid():
            c = ExpresFiles.objects.create(
                email = ema,
                description = desc,
                slug = random_slug
            )
            f = FilesExpres.objects.create(
                expresfile = c,
                files_s = f
            )

            print('OK expres files seve')
            print()
            messages.success(request, "Файл добавлен. Ожидайте письмо с ключем доступа для скачивания", extra_tags="alert-success")
            mess = 'Ваш email:'+' '+ ema + ' был использован для загрузки файлов.'+ \
                   ' Ключь доступа: ' + c.slug
            from_email = ema
            send_mail('Спасибо что выбрали нас!', mess, settings.EMAIL_HOST_USER, [from_email], fail_silently=False)
            c.save()
            f.save()
            return redirect('/')

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
