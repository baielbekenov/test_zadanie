from django.contrib import admin

from apps.orders.models import Order, Payment, Coordinates, Contact, Address

# Register your models here.


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Coordinates)
admin.site.register(Contact)
admin.site.register(Address)