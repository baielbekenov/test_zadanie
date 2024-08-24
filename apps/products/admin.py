from django.contrib import admin

from apps.products.models import Product, Image, Cart, CartItems, Orders

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Orders)
