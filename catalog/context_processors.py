from .models import Category

def category(request):
    args = {}
    args['categories'] = Category.objects.filter(is_publish=True)
    args['category_verbos_name'] = Category._meta.verbose_name
    return args

def verbos_name_catalog(request):
    return {'verbose_name_category'}
