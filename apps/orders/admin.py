from django.contrib import admin

from apps.orders.models import Order, Payment, Coordinates, Contact, Address

# Register your models here.


admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Coordinates)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'phone')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'cityName', 'rawAddress', 'pickup', 'coordinates', )