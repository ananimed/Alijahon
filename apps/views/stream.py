from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, DetailView

from apps.forms import OrderForm, StreamForm
from apps.models import Product, Stream, SiteSettings


class StreamFormView(LoginRequiredMixin, FormView):
    form_class = StreamForm
    template_name = 'apps/stream/product-market.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return redirect('stream-list')

    def form_invalid(self, form):
        print(form)


class StreamListView(ListView):
    queryset = Stream.objects.all()
    template_name = 'apps/stream/stream-list.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class StreamStatisticDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/stream/stream-statistics.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['self_stream'] = Stream.objects.filter(product=self.object, owner=self.request.user)
        return context


class StreamOrderView(DetailView, FormView):
    form_class = OrderForm
    queryset = Stream.objects.all()
    template_name = 'apps/trade/product-detail.html'
    context_object_name = 'stream'

    def form_valid(self, form):
        if form.is_valid():
            form = form.save(commit=False)
            form.stream = self.get_object()
            form.user = self.request.user
            form.save()
            # Adjust product price
            form.product.price -= self.get_object().discount

            # Retrieve and set deliver_price safely
            site_settings = SiteSettings.objects.first()
            if site_settings:
                form.deliver_price = site_settings.deliver_price
            else:
                form.deliver_price = 0  # Or some default value

        return render(self.request, 'apps/order/product-order.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object.product
        product.price -= self.object.discount
        context['product'] = product

        # Handle SiteSettings potentially being None
        site_settings = SiteSettings.objects.first()
        if site_settings:
            context['deliver_price'] = site_settings.deliver_price
        else:
            context['deliver_price'] = 0  # Or some default value

        stream_id = self.kwargs.get('pk')
        Stream.objects.filter(pk=stream_id).update(count=F('count') + 1)

        return context