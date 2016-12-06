from django.contrib import admin
from .models import Category, Catalog, Files

class FilesInLine(admin.StackedInline):
    model = Files
    extra = 2

class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class CatalogAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields':['title',
                          'category',
                          'user',
                          'description']}),
        ('Дата добавления', {'fields': ['date_add'], 'classes': ['collapse']}),
        ('Доступ к файлу', {'fields':['is_open',
                                      'is_slug',
                                      'is_for_me']})
    ]
    inlines = [FilesInLine]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Catalog, CatalogAdmin)


