from .models import Category
from .forms import SearchForm
def category(request):
    args = {}
    args['categories'] = Category.objects.filter(is_publish=True)
    args['category_verbos_name'] = Category._meta.verbose_name
    args['search']= SearchForm()
    return args