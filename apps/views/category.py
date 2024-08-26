
from django.views.generic import ListView

from apps.models import Product, Category


class CategoryListView(ListView):
    queryset = Product.objects.all().select_related('category')
    template_name = 'apps/trade/home-page.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['categories'] = Category.objects.all()
        return data
