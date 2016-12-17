# -*- coding: utf-8 -*-
import os

from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.http import HttpResponse
from django.template import RequestContext
from django.template.context_processors import csrf
from django.shortcuts import render, redirect, render_to_response

from catalog.forms import ExpresFilesForms, FilesExpresForms, TestForm, SearchForm, SearchKey, AddCatalogForm, \
    FilesCatalogForms, CatalogForms
from fenix import settings
from .models import Category, Catalog, FilesCatalog, FilesExpres, ExpresFiles

from django.contrib.auth.models import UserManager
import re
from django.db.models import Q

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
                           ' Ключ доступа: ' + c.slug + '\n' + 'Или перейдите по ссылке: ' + 'http://'+ url_site + '/get-' + c.slug
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
        return render(request, '../templates/catalog/category.html', args)
    except Category.DoesNotExist:
        raise Http404


def view_details(request, slug):
    args={}
    args.update(csrf(request))
    try:
        a=[]
        args['username'] = auth.get_user(request).username
        args['title']=Catalog.objects.get(slug=slug).title
        args['catalog']= Catalog.objects.get(slug=slug, is_open=True)
        args['files'] = FilesCatalog.objects.filter(catalog=Catalog.objects.get(slug=slug, is_open=True))
        for i in args['files']:
            a.append({'file': {'id': i.id, 'name': str(i.files_s).split('/')[3]}})
        args['files_m'] = a
        return render(request, '../templates/catalog/view_details.html', args)
    except Catalog.DoesNotExist:
        raise Http404

# Get LINK
def view_expresfile(request, slug):
    args={}
    args.update(csrf(request))
    try:
        a = []
        args['title'] = ExpresFiles.objects.get(slug=slug).email
        args['expres_file']= ExpresFiles.objects.filter(slug=slug)
        args['files'] = FilesExpres.objects.filter(expresfile_id = ExpresFiles.objects.get(slug=slug))
        for i in args['files']:
            a.append({'file': {'id': i.id, 'name': str(i.files_s).split('/')[3]}})
        args['files_m'] = a
        return render(request, '../templates/catalog/views_expresfile.html', args)
    except ExpresFiles.DoesNotExist:
        raise Http404

# Get KEY
def search_key(request):
    args = {}
    args.update(csrf(request))
    args['form_search_key'] = SearchKey()
    if request.POST:
        g = SearchKey(request.POST)#request.POST.get('search', '')
        if g.is_valid():
            a = []
            try:
                args['title'] = ExpresFiles.objects.get(slug=g.cleaned_data['s_key']).email
                args['expres_file'] = ExpresFiles.objects.filter(slug=g.cleaned_data['s_key'])
                args['files'] = FilesExpres.objects.filter(expresfile_id=ExpresFiles.objects.get(slug=g.cleaned_data['s_key']))
                print(args['files'].count())
                for i in args['files']:
                    a.append({'file':{'id': i.id, 'name': str(i.files_s).split('/')[3]}})
                args['files_m']= a
                return render(request, '../templates/catalog/views_expresfile.html', args)
            except ExpresFiles.DoesNotExist:
                messages.error(request, "Файл с таким ключем не найден!", extra_tags="alert-danger")
                return redirect('/')
        else:
            return redirect('/')
    return render(request, '../templates/catalog/views_expresfile.html', args)

# download file expres
def download_link(request, slug, file_id):
    url_site = request.META['HTTP_HOST']
    try:
        file = FilesExpres.objects.filter(expresfile_id=ExpresFiles.objects.get(slug=slug).id)
        for f in file:
            file_name = (f.files_s.name.split('/')[3]).split('.')[0]
            file_path = os.path.join(f.files_s.path)
            f_type = f.files_s.path.split('.')[-1]
            f_email = ExpresFiles.objects.get(slug=slug).email
            f = open(file_path, 'rb')
            response = HttpResponse(f, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % url_site+'_'+ file_name + '.' + f_type
            return response
    except FilesExpres.DoesNotExist:
        raise Http404

# download file catalog
def download_d(request, slug, file_id):
    try:
        url_site = request.META['HTTP_HOST']
        file = FilesCatalog.objects.filter(catalog_id=Catalog.objects.get(slug=slug).id)
        for f in file:
            file_name = (f.files_s.name.split('/')[3]).split('.')[0]
            file_path = os.path.join(f.files_s.path)
            f_type = f.files_s.path.split('.')[-1]
            f_d = Catalog.objects.get(slug=slug)
            f = open(file_path, 'rb')
            response = HttpResponse(f, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % url_site+'_'+ file_name + '.' + f_type
            return response
    except FilesCatalog.DoesNotExist:
        raise Http404

def myfiles(request, user_id):
    args={}
    args.update(csrf(request))
    args['username']= auth.get_user(request).username
    args['title']= 'Мои файлы'
    args['catalog'] = Catalog.objects.filter(category__is_publish=True, user_id=auth.get_user(request).id).order_by('-date_add')
    return render(request, '../templates/catalog/myfiles.html', args)

def addfile(request):
    args={}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    args['title'] = 'Добаввть файл'
    args['form_c'] = CatalogForms()#AddCatalogForm()
    args['form_f'] = FilesCatalogForms()
    return render(request, '../templates/catalog/addfiles.html', args)

def get_addfile(request):
    args = {}
    url_site = request.META['HTTP_HOST']
    args.update(csrf(request))
    return_path = request.META.get('HTTP_REFERER', '/')
    args['form_c'] = CatalogForms()
    args['form_f'] = FilesCatalogForms()
    if request.POST:
        form_c = CatalogForms(request.POST, request.FILES)
        form_f = FilesCatalogForms(request.FILES)
        if form_c.is_valid():
            form_c.instance.user =request.user
            form_c.save()
            gn = FilesCatalog.objects.create(
                catalog = Catalog.objects.get(id=form_c.instance.id),
                files_s = request.FILES.get('files_s','')
            )
            gn.save()

            if form_c.instance.is_slug == True:
                mess = 'Вы загрузили файлы. При этом выбрав пукт доступа к файлу "Доступ по ссылке". ' + \
                       'Перейдите по ссылке: ' + 'http://' + url_site + '/slug-' + form_c.instance.slug
                from_email = auth.get_user(request).email
                send_mail('Загрузка файлов', mess, settings.EMAIL_HOST_USER, [from_email],
                          fail_silently=False)


            print(form_c.instance.is_for_me)
            messages.success(request, "Файл добавлен.",
                             extra_tags="alert-success")
            return redirect('/')
        else:
            messages.error(request, "Файл не добавлен.",
                             extra_tags="alert-danger")
            return redirect(return_path)
    return redirect('/')

def view_details_slug(request, slug):
    args={}
    args.update(csrf(request))
    try:
        a=[]
        args['username'] = auth.get_user(request).username
        args['title']=Catalog.objects.get(slug=slug).title
        args['catalog']= Catalog.objects.get(slug=slug, is_slug=True)
        args['files'] = FilesCatalog.objects.filter(catalog=Catalog.objects.get(slug=slug, is_slug=True))
        for i in args['files']:
            a.append({'file': {'id': i.id, 'name': str(i.files_s).split('/')[3]}})
        args['files_m'] = a
        return render(request, '../templates/catalog/view_details.html', args)
    except Catalog.DoesNotExist:
        raise Http404


# SEARCH
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    args={}
    args['query_string'] = ''
    args['query_string'] = None
    args['query_string'] = request.GET['search']
    if (args['query_string']).isupper:
        query_string=(args['query_string']).lower()
        entry_query = get_query(query_string, [('title').lower(), ('description').lower(), ])
    else:
        query_string = (args['query_string']).upper()
        entry_query = get_query(query_string, [('title').upper(), ('description').upper(), ])

    args['found_entries'] = Catalog.objects.filter(entry_query, is_open=True).order_by('-date_add')

    return render(request, '../templates/catalog/search_result.html', args)

# END SEARCH

