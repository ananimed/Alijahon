from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.utils.html import format_html

from apps.models import User, Category, ProductImage, Product, Order

admin.site.site_header = "Alijahon Admin"
admin.site.site_title = "Welcome Alijahon "
admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    exclude = 'slug',
    list_display = 'id', 'name', 'image_photo'

    @admin.display(empty_value='')
    def image_photo(self, obj):
        photo = obj.image
        return format_html("<img src='{}' style-'width: 50px' />", photo)

    @admin.display(empty_value='')
    def product_count(self, obj):
        return obj.product_count()


class ProductImageInline(StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    exclude = 'slug',
    inlines = [ProductImageInline]
    list_display = 'name', 'is_exits'
    search_fields = ['name', 'price']
    ordering = '-created_at',
    list_filter = 'quantity',

    @admin.display(empty_value='')
    def is_exits(self, obj):
        icon_url = 'https://img.icons8.com/?size=100&id=9fp9k4lPT8us&format=png&color=000000'
        if not obj.quantity:
            icon_url = 'https://img.icons8.com/?size=100&id=63688&format=png&color=000000'
        return format_html("<img src='{}' style='width: 30px' />", icon_url)


