from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.views.generic import ListView
from django.views.generic import TemplateView, FormView

from apps.models import Category, Product, Stream, User, Order



class MarketListView(ListView):
    template_name = 'apps/stream/product-market.html'
    queryset = Category.objects.all()
    context_object_name = 'categories'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()
        if slug := self.request.GET.get("category"):
            products = products.filter(category__slug=slug)
        data['products'] = products
        return data


class AdminPageView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/admin_page.html'


class WithdrawView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/withdraw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AdminPageStatisticsListView(ListView):
    queryset = Stream.objects.all()
    template_name = 'admin/statistics.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return (
            Stream.objects.filter(owner=self.request.user).annotate(
                new_count=Count('orders', filter=Q(orders__status=Order.StatusType.NEW)),
                ready_count=Count('orders', filter=Q(orders__status=Order.StatusType.READY)),
                deliver_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVER)),
                delivered_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED)),
                cant_phone_count=Count('orders', filter=Q(orders__status=Order.StatusType.CANT_PHONE)),
                canceled_count=Count('orders', filter=Q(orders__status=Order.StatusType.CANCELED)),
                archived_count=Count('orders', filter=Q(orders__status=Order.StatusType.ARCHIVED)),
            ).values(
                'name', 'product__name', 'count',
                'new_count', 'ready_count', 'deliver_count',
                'delivered_count', 'cant_phone_count',
                'canceled_count', 'archived_count'
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_queryset().aggregate(
                all_count=Sum('count'),
                all_new=Sum('new_count'),
                all_ready=Sum('ready_count'),
                all_deliver=Sum('deliver_count'),
                all_delivered=Sum('delivered_count'),
                all_cant_phone=Sum('cant_phone_count'),
                all_canceled=Sum('canceled_count'),
                all_archived=Sum('archived_count'),
            )
        )
        return context


class AdminCompetitionView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin/competition.html'
    context_object_name = 'delivered_orders'

    def get_queryset(self):
        return (
            User.objects.annotate(
                order_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED))
            )
            .filter(order_count__gt=0)
            .order_by('-order_count')
        )


class AdminRequestsView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/requests.html'


class AdminProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/profile.html'


class AdminSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/settings.html'
