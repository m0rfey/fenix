# -*- coding: utf-8 -*-

from django.db import models

from fenix.settings import MEDIA_ROOT
from userprofile.models import User
from sorl.thumbnail import ImageField, get_thumbnail, fields
import datetime


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
    return '%s/%s/%s/cover/%s' % (datetime.datetime.now().year, instance.user_id, instance.category.slug, filename)

class Catalog(models.Model):
    cover = ImageField(verbose_name='Постер', upload_to=upload_cover)
    thumb_cover = ImageField(upload_to='media/')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    category = models.ForeignKey(Category, verbose_name='Категория')
    user = models.ForeignKey(User, verbose_name='Автор')
    description = models.TextField(verbose_name='Описание', max_length=300)
    slug = models.SlugField(verbose_name='Алиас')
    is_open = models.BooleanField(verbose_name='Для всех', help_text='Дать доступ к файлу для всех пользователей')
    is_slug = models.BooleanField(verbose_name='По ссылке', help_text='Файл будет доступет только по ссылке')
    is_for_me = models.BooleanField(verbose_name='Только для меня', help_text='Файл будет доступен только Вам')

    def save(self, *args, **kwargs):
        if self.cover:
            self.thumb_cover = get_thumbnail(self.cover, '150x200', quality=95).url
        super(Catalog, self).save(*args, **kwargs)

    class Meta:
        db_table = 'catalog'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title

class ExpresFiles(models.Model):
    email = models.EmailField(verbose_name='Email')
    #category = models.ForeignKey(Category, default=Category.objects.get(id=1))
    slug = models.SlugField(verbose_name='Алиас')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        db_table = 'expresfiles'
        verbose_name = 'Временные файлы'
        verbose_name_plural = 'Временные файлы'

    def __str__(self):
        return self.email


def upload_file(instance, filename):
    d = datetime.datetime.now()
    if instance.catalog:
        m = instance.catalog.user_id
        c = instance.catalog.category.slug
    elif instance.expresfile:
        m = instance.expresfile.email
        c = instance.expresfile.slug
    else:
        m = 0
        c = 0


    return '%s/%s/%s/%s' % (d.year, m, c, filename)

class Files(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE,blank=True, null=True)
    expresfile = models.ForeignKey(ExpresFiles, verbose_name='Временные файлы', blank=True, null=True)
    files_s = models.FileField(verbose_name='Файл', upload_to=upload_file)
    slug = models.SlugField(verbose_name='Алиас')

    class Meta:
        db_table = 'files'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
    def __str__(self):
        return str(self.files_s)