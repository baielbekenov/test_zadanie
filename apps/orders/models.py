from django.db import models

from apps.products.models import Cart
from apps.user.models import User

# Create your models here.


class Order(models.Model):
    PENDING = 'pending'
    PROCESSED = 'processed'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSED, 'Processed'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id} for {self.user_id}'


class Payment(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (FAILED, 'Failed')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[('card', 'Card'), ('cash', 'Cash on Delivery')], default='card')
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    currency_code = models.CharField(max_length=3, default='EUR')
    is_cash_on_delivery = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=50, choices=[('glovo', 'Glovo'), ('other', 'Other')])
    delivery_address = models.CharField(max_length=255)
    delivery_address_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_address_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    recipient_phone = models.CharField(max_length=15)
    recipient_name = models.CharField(max_length=50, blank=True, null=True)
    pickup_address = models.CharField(max_length=255, verbose_name="Pickup address")
    pickup_phone = models.CharField(max_length=15, verbose_name="Pickup phone")
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def send_to_glovo(self):
        """
        Логика для отправки заказа в Glovo API
        """
        # Данные для API Glovo
        glovo_data = {
            "address": {
                "lat": self.delivery_address_latitude,
                "lon": self.delivery_address_longitude,
                "label": self.delivery_address
            },
            "contact": {
                "phoneNumber": self.recipient_phone,
                "name": self.recipient_name or "Anonymous"
            },
            "packageDetails": {
                "description": "Order description"
            },
            "packageId": str(self.order.id),
            "pickupDetails": {
                "address": self.pickup_address,
                "contact": {
                    "phoneNumber": self.pickup_phone,
                    "name": "Store Contact"
                }
            },
            "price": {
                "amount": float(self.order.total_price) if self.order.payment.is_cash_on_delivery else None,
                "currency": self.order.payment.currency_code if self.order.payment.is_cash_on_delivery else None
            }
        }