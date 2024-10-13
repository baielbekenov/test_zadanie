from django.contrib import admin

from apps.products.models import Product, Cart, CartItems


@admin.register(Product)
class ProductcAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight')


admin.site.register(Cart)
admin.site.register(CartItems)

