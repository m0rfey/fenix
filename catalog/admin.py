from django.contrib import admin
from .models import Category, Catalog, Files, ExpresFiles


class FilesInLine(admin.StackedInline):
    model = Files
    fields = ['files_s', 'slug']
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
                          'description']}),
        #('Дата добавления', {'fields': ['date_add'], 'classes': ['collapse']}),
        ('Доступ к файлу', {'fields':['is_open',
                                      'is_slug',
                                      'is_for_me']})
    ]
    inlines = [FilesInLine]

class ExpresFilesAdmin(admin.ModelAdmin):
    fields = ['email', 'slug']
    list_display = ['email', 'date_add', 'slug']
    list_filter = ['email', 'date_add']

    inlines = [FilesInLine]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(ExpresFiles, ExpresFilesAdmin)

