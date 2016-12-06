# -*- coding: utf-8 -*-

from django.db import models

from userprofile.models import User
import datetime


class Category(models.Model):
    name= models.CharField(max_length=20)
    slug = models.SlugField()

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural='Категории'

    def __str__(self):
        return self.name

class Catalog(models.Model):
    cover = models.ImageField(verbose_name='Постер', upload_to='media/cover')
    date_add = models.DateTimeField(verbose_name='Дата')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    category = models.ForeignKey(Category, verbose_name='Категория')
    user = models.ForeignKey(User, verbose_name='Автор')
    description = models.TextField(verbose_name='Описание', max_length=300)
    is_open = models.BooleanField(verbose_name='Для всех', help_text='Дать доступ к файлу для всех пользователей')
    is_slug = models.BooleanField(verbose_name='По ссылке', help_text='Файл будет доступет только по ссылке')
    is_for_me = models.BooleanField(verbose_name='Только для меня', help_text='Файл будет доступен только Вам')

    class Meta:
        db_table = 'catalog'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title

def upload_file(instance, filename):
    d = datetime.datetime.now()
    return '%s/%s/%s/%s' % (d.year, instance.catalog.user_id, instance.catalog.category_id, filename)

class Files(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    files_s = models.FileField(verbose_name='Файл', upload_to=upload_file)
    slug = models.SlugField()

    class Meta:
        db_table = 'files'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

