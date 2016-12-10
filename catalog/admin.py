# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Category, Catalog, FilesCatalog, ExpresFiles, FilesExpres


class FilesCatalogInLine(admin.StackedInline):
    model = FilesCatalog
    fields = ['files_s']
    extra = 2

class FilesExpresInLine(admin.StackedInline):
    model = FilesExpres
    fields = ['files_s']
    extra = 2

class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class CatalogAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields':['title',
                          'cover',
                          'category',
                          'user',
                          'slug',
                          'description']}),
        #('Дата добавления', {'fields': ['date_add'], 'classes': ['collapse']}),
        ('Доступ к файлу', {'fields':['is_open',
                                      'is_slug',
                                      'is_for_me']})
    ]
    inlines = [FilesCatalogInLine]

class ExpresFilesAdmin(admin.ModelAdmin):
    fields = ['email', 'slug', 'description']
    list_display = ['email', 'date_add', 'slug']
    list_filter = ['email', 'date_add']

    inlines = [FilesExpresInLine]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(ExpresFiles, ExpresFilesAdmin)

