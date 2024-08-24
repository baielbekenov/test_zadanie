from django.db import models

from apps.category.models import Category
from apps.user.models import User


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                    blank=True, null=True, verbose_name='Категории', related_name='productcategory')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


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
                                           blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.user_id)

    def save(self, *args, **kwargs):
        self.total_cart_price = sum(item.total_item_price for item in self.cartitems_set.all())
        super().save(*args, **kwargs)


class CartItems(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='cartitems')
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена товара')
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая стоимость позиции',
                                           blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'ТоварВКорзине'
        verbose_name_plural = 'ТоварыВКорзине'

    def save(self, *args, **kwargs):
        self.total_item_price = self.quantity * self.price
        super().save(*args, **kwargs)


select = ((1, 'Glovo'),
          (2, 'Яндекс.Доставка'),
          )


class Orders(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    cart_id = models.ForeignKey(
        Cart,
        on_delete=models.PROTECT,
        verbose_name='Корзина'
    )
    delivery_method = models.IntegerField(choices=select, verbose_name='Способ доставки', blank=True, null=True)
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    recipient_phone = models.CharField(max_length=15, verbose_name='Телефон получателя')
    comments = models.TextField(blank=True, verbose_name='Комментарии к доставке')
    status = models.CharField(max_length=50, verbose_name='Статус заказа')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая цена')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id} for {self.user_id}'


