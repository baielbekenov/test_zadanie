from django.db import models

from apps.products.models import Cart
from apps.user.models import User

# Create your models here.


class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Долгота")

    class Meta:
        verbose_name = 'Координат'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return f"Lat: {self.latitude}, Lon: {self.longitude}"


class Address(models.Model):
    cityName = models.CharField(max_length=100, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")
    postalCode = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    rawAddress = models.CharField(max_length=255, verbose_name="Полный адрес")
    pickup = models.BooleanField(verbose_name='Точка вывоза', default=False)
    details = models.TextField(verbose_name="Дополнительные детали", blank=True, null=True)
    streetName = models.CharField(max_length=255, verbose_name="Улица")
    streetNumber = models.CharField(max_length=20, verbose_name="Номер дома")
    coordinates = models.OneToOneField(Coordinates, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Координаты")

    def __str__(self):
        return f"{self.rawAddress}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = 'Контактные данные'
        verbose_name_plural = 'Контактные данные'

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Order(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.PROTECT)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="delivery_address")
    pickup_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="pickup_address")
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id} for {self.order_id}'


class Payment(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (FAILED, 'Failed')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_payment")
    payment_method = models.CharField(max_length=50, choices=[('card', 'Card'), ('cash', 'Cash on Delivery')], default='card')
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='KGS')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'



