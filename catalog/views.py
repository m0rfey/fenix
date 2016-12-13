# -*- coding: utf-8 -*-
import os

from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.shortcuts import render, redirect


from catalog.forms import ExpresFilesForms, FilesExpresForms, TestForm, SearchForm, SearchKey
from fenix import settings
from .models import Category, Catalog, FilesCatalog, FilesExpres, ExpresFiles

from formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import UserManager

def index(request):
    args={}
    args['title'] = 'Home'
    args['catalog'] = Catalog.objects.filter(is_open=True, category__is_publish=True).order_by('-date_add')
    args['expres_form'] = TestForm()
    args['form_search_key'] = SearchKey()
    args['username'] = auth.get_user(request).username
    return render(request, '../templates/catalog/index.html', args)

def expres_save(request):
    args={}
    return_path = request.META.get('HTTP_REFERER', '/')
    url_site = request.META['HTTP_HOST']
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    args['expres_form'] = TestForm()
    f_type = ['jpg', 'jpeg', 'JPG', 'JPEG', 'PNG', 'png', 'mkv', 'avi',
              'flv', 'pdf', 'mp4', 'mp3', 'flac', 'rar', 'zip',
              'djvu', 'doc', 'docx', 'txt', 'fb2', 'xls', 'xlsx',
              'wav', 'wma', 'mpg', 'mpeg', 'wmv', 'iso', 'mdf', 'mds']
    if request.POST:
        ema =request.POST.get('email','')
        desc= request.POST.get('description', '')
        f = request.FILES.get('files_s', '')
        form = TestForm(request.POST, request.FILES)
        random_slug = UserManager().make_random_password(length=25)
        if form.is_valid():
            mes = 0
            for i in f_type:
                if i == str(f).split('.')[-1]:
                    c = ExpresFiles.objects.create(
                        email = ema,
                        description = desc,
                        slug = random_slug
                    )
                    f = FilesExpres.objects.create(
                        expresfile = c,
                        files_s = f
                    )
                    c.save()
                    f.save()
                    print('OK expres files seve')
                    print()
                    messages.success(request, "Файл добавлен. Ожидайте письмо с ключем доступа для скачивания",
                                     extra_tags="alert-success")
                    mess = 'Ваш email:' + ' ' + ema + ' был использован для загрузки файлов.' + \
                           ' Ключ доступа: ' + c.slug + '\n' + 'Или перейдите по ссылке: ' + 'http://'+ url_site + '/' + c.slug
                    from_email = ema
                    send_mail('Спасибо что выбрали нас!', mess, settings.EMAIL_HOST_USER, [from_email],
                              fail_silently=False)

                    return redirect('/')
                else:
                    mes += 1
            if mes > 0:
                messages.error(request, "Файл не подходит ни под одно расширение! Разрешенные файлы %s" % f_type, extra_tags="alert-danger")
                return redirect(return_path)

    return render(request, '../templates/catalog/index.html', args)

def category(request, category_slug):
    args={}
    args['username'] = auth.get_user(request).username
    try:
        args['title'] = Category.objects.get(slug = category_slug)
        args['category'] = Catalog.objects.filter(category=Category.objects.get(slug=category_slug), is_open=True).order_by('-date_add')
    except Category.DoesNotExist:
        raise Http404
    return render(request, '../templates/catalog/category.html', args)

def view_details(request, slug):
    args={}
    args.update(csrf(request))
    try:
        args['username'] = auth.get_user(request).username
        args['title']=Catalog.objects.get(slug=slug).title
        args['catalog']= Catalog.objects.get(slug=slug, is_open=True)
        args['files'] = FilesCatalog.objects.filter(catalog=Catalog.objects.get(slug=slug, is_open=True))
    except Catalog.DoesNotExist:
        raise Http404
    return render(request, '../templates/catalog/view_details.html', args)


def view_expresfile(request, slug):
    args={}
    args.update(csrf(request))
    args['title'] = ExpresFiles.objects.get(slug=slug).email
    args['expres_file']= ExpresFiles.objects.filter(slug=slug)
    args['files'] = FilesExpres.objects.filter(expresfile_id = ExpresFiles.objects.get(slug=slug))
    return render(request, '../templates/catalog/views_expresfile.html', args)


def search_key(request):
    args = {}
    args.update(csrf(request))
    args['form_search_key'] = SearchKey()
    if request.POST:
        g = SearchKey(request.POST)#request.POST.get('search', '')
        if g.is_valid():
            try:
                args['title'] = ExpresFiles.objects.get(slug=g.cleaned_data['s_key']).email
                args['expres_file'] = ExpresFiles.objects.filter(slug=g.cleaned_data['s_key'])
                args['files'] = FilesExpres.objects.filter(expresfile_id=ExpresFiles.objects.get(slug=g.cleaned_data['s_key']))
                return render(request, '../templates/catalog/views_expresfile.html', args)
            except ExpresFiles.DoesNotExist:
                messages.error(request, "Файл с таким ключем не найден!", extra_tags="alert-danger")
                return redirect('/')
        else:
            return redirect('/')
    return render(request, '../templates/catalog/expresfiles.html', args)

def download_link(request, slug, file_id):
    url_site = request.META['HTTP_HOST']
    file = FilesExpres.objects.filter(expresfile_id=ExpresFiles.objects.get(slug=slug).id)
    for f in file:
        file_path = os.path.join(f.files_s.path)
        f_type = f.files_s.path.split('.')[-1]
        f_email = ExpresFiles.objects.get(slug=slug).email
        f = open(file_path, 'rb')
        response = HttpResponse(f, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % url_site+'-'+f_email + '-'+ slug + '_'+ file_id + '.' + f_type
        return response

def download_d(request, slug, file_id):
    print(file_id)
    url_site = request.META['HTTP_HOST']
    file = FilesCatalog.objects.filter(catalog_id=Catalog.objects.get(slug=slug).id)
    for f in file:
        file_path = os.path.join(f.files_s.path)
        print(file_path)
        f_type = f.files_s.path.split('.')[-1]
        f_d = Catalog.objects.get(slug=slug)
        print(f_d.category.slug)
        f = open(file_path, 'rb')
        response = HttpResponse(f, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % url_site+'-'+f_d.user.username +'_'+ f_d.category.slug + '-'+ slug + '_'+ file_id + '.' + f_type
        return response
