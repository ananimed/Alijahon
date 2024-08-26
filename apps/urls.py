from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('product/list', ProductListView.as_view(), name='product_list'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('wishlist', WishListView.as_view(), name='wishlist'),
    path('product/liked/<str:slug>', LikeProductView.as_view(), name='liked'),
    path('product/order-list', OrderListView.as_view(), name='order-list'),
    path('search/', search_products, name='search_products')
]

urlpatterns += [
    path('stream/form', StreamFormView.as_view(), name='stream-form'),
    path('stream/list', StreamListView.as_view(), name='stream-list'),
    path('stream/statistics/<str:slug>/', StreamStatisticDetailView.as_view(), name='stream-statistics'),
    path('oqim/<int:pk>', StreamOrderView.as_view(), name='oqim'),

]

urlpatterns += [
    path('admin_page/profile/', AdminProfileView.as_view(), name='admin-page-profile'),
    path('admin_page/settings/', AdminSettingsView.as_view(), name='admin-page-settings'),
    path('market/', MarketListView.as_view(), name='market-list'),
    path('admin_page', AdminPageView.as_view(), name='admin-page'),
    path('admin_page/withdraw', WithdrawView.as_view(), name='admin-page-withdraw'),
    path('admin_page/statistics', AdminPageStatisticsListView.as_view(), name='admin-page-statistics'),
    path('admin_page/competition', AdminCompetitionView.as_view(), name='admin-page-competition'),
    path('admin_page/request', AdminRequestsView.as_view(), name='admin-page-request'),
   ]
