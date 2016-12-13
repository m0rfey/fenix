#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from sorl.thumbnail import ImageField, get_thumbnail, fields


def upload_avatar(instance, filename):
    return "media/avatars/%s/%s" %(instance, filename)

class User(AbstractUser):
    avatar = ImageField(null=True, blank=True, upload_to=upload_avatar, verbose_name='Аватар')
    #email = models.EmailField(unique=True)
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'userprofile'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
