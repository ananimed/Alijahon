from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, FormView, DetailView

from apps.forms import OrderForm
from apps.models import Category, Product, WishList


class ProductListView(ListView):
    queryset = Product.objects.all().prefetch_related('images')
    template_name = 'apps/trade/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cat_slug = self.request.GET.get("category")
        query = super().get_queryset()
        if cat_slug:
            query = query.filter(category__slug=cat_slug)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data


class ProductDetailView(DetailView, FormView):
    form_class = OrderForm
    model = Product
    template_name = 'apps/trade/product-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save()
        return render(self.request, 'apps/order/product-order.html', {'form': form})


class WishListView(LoginRequiredMixin, ListView):
    queryset = WishList.objects.all()
    template_name = 'apps/wishlist.html'
    paginate_by = 10
    context_object_name = "wishlists"

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user)
        return query


class LikeProductView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('slug'))
        obj, created = WishList.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.delete()
            return JsonResponse({'save': 0})
        return JsonResponse({'save': 1})




def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'apps/search/search.html', {'products': products, 'query': query})
