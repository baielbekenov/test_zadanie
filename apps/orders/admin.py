from django.contrib import admin

from apps.orders.models import Order, Payment, Delivery

# Register your models here.


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Delivery)