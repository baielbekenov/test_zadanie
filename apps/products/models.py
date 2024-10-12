from django.db import models

from apps.category.models import Category
from apps.user.models import User

size = ((1, ('маленький')),
        (2, ('средний')),
        (3, ('большой')),
        )


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                    blank=True, null=True, verbose_name='Категории', related_name='productcategory')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес (кг)', blank=True, null=True)
    size = models.IntegerField(choices=size, verbose_name='Размер', default=1)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')
    ordering = models.PositiveIntegerField(verbose_name='Порядок', default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.ordering == 0:
            last_product = Product.objects.order_by('-ordering').first()
            if last_product:
                self.ordering = last_product.ordering + 1
            else:
                self.ordering = 1
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='images/posts/%Y/%m', blank=True, null=True, verbose_name='Фото')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='productimages', verbose_name='Продукты')

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'

    def __str__(self):
        return str(self.product_id)


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    total_cart_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость корзины',
                                           default=0)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user_id'], name='unique_cart_per_user')

        ]

    def calculate_total_price(self):
        return sum(item.total_item_price for item in self.cartitems.all())

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        self.total_cart_price = self.calculate_total_price()
        return super().save(update_fields=['total_cart_price'])


class CartItems(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='cartitems')
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                verbose_name='Цена товара')
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая стоимость позиции',
                                           default=0)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'ТоварВКорзине'
        verbose_name_plural = 'ТоварыВКорзине'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.total_item_price = self.quantity * self.price
        super().save(*args, **kwargs)



