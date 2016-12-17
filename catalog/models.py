# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify

from fenix.settings import MEDIA_ROOT
from userprofile.models import User
from sorl.thumbnail import ImageField, get_thumbnail, fields
import datetime
from django.contrib.auth.models import UserManager


def randomStr():
    return str(datetime.datetime.now().year)+'-'+(UserManager().make_random_password(length=25))

class Category(models.Model):
    name= models.CharField(max_length=20)
    slug = models.SlugField(verbose_name='Алиас')
    is_publish = models.BooleanField(verbose_name='Опубликовать', default=False)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural='Категории'

    def __str__(self):
        return self.name

def upload_cover(instance, filename):
    return u'%s/%s/%s/cover/%s' % (datetime.datetime.now().year, instance.user_id, instance.category.slug, filename)
CHOICES = [('is_open', 'Опубликован'),
           ('is_slug', 'Доступ по ссылке'),
           ('is_for_me', 'Только для меня')]
class Catalog(models.Model):
    cover = ImageField(verbose_name='Постер', upload_to=upload_cover)
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    category = models.ForeignKey(Category, verbose_name='Категория')
    user = models.ForeignKey(User, verbose_name='Автор')
    description = models.TextField(verbose_name='Описание', max_length=300)
    slug = models.SlugField(verbose_name='Алиас', default=randomStr, unique=True)
    # is_open = models.BooleanField(verbose_name='Для всех', help_text='Дать доступ к файлу для всех пользователей')
    # is_slug = models.BooleanField(verbose_name='По ссылке', help_text='Файл будет доступен только по ссылке')
    # is_for_me = models.BooleanField(verbose_name='Только для меня', help_text='Файл будет доступен только Вам')
    choices = models.CharField(choices=CHOICES, max_length=11, verbose_name='Публикация' )

    class Meta:
        db_table = 'catalog'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title

class ExpresFiles(models.Model):
    email = models.EmailField(verbose_name='Email')
    description = models.TextField(verbose_name='Описание',max_length=300)
    slug = models.SlugField(verbose_name='Алиас', blank=True, null=True, default=randomStr, unique=True)#max_length=25
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')

    class Meta:
        db_table = 'expresfiles'
        verbose_name = 'Временные файлы'
        verbose_name_plural = 'Временные файлы'

    def __str__(self):
        return self.email

def upload_file_catalog(instance, filename):
    d = datetime.datetime.now()
    if instance.catalog:
        m = instance.catalog.user_id
        c = instance.catalog.slug
    else:
        m = 0
        c = 0
    return u'%s/%s/%s/%s' % (d.year, m, c, filename)

def upload_file(instance, filename):
    d = datetime.datetime.now()
    if instance.expresfile:
        m = instance.expresfile.email
        c = instance.expresfile.slug
    else:
        m = 0
        c = 0
    return u'%s/%s/%s/%s' % (d.year, m, c, filename)

class FilesCatalog(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, blank=True, null=True)
    files_s = models.FileField(verbose_name='Файл', upload_to=upload_file_catalog)

    class Meta:
        db_table = 'files_catalog'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
    def __str__(self):
        return str(self.files_s)

class FilesExpres(models.Model):
    expresfile = models.ForeignKey(ExpresFiles, verbose_name='Временные файлы', on_delete=models.CASCADE, blank=True, null=True)
    files_s = models.FileField(verbose_name='Файл', upload_to=upload_file)

    class Meta:
        db_table = 'files_expres'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return str(self.files_s)