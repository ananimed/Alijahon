from django.views.generic import ListView

from apps.models import Order


class OrderListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/order/order-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user)
        return query

#
# class OrderRequestListView(ListView):
#     queryset = Order.objects.all()
#     template_name = 'admin/requests.html'
#     context_object_name = 'orders'
#
#     def get_queryset(self):
#