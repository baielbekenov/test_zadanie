from django.contrib import admin

from apps.products.models import Product, Image, Cart, CartItems


@admin.register(Product)
class ProductcAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'price', 'weight', 'ordering')


admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(CartItems)

