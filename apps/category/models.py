from django.db import models


class Banner(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', default='Здесь должно быть название баннера')
    image = models.ImageField(upload_to='banners/%Y/%m', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    url = models.URLField()

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, verbose_name='Название')
    image = models.ImageField(upload_to='images/category/%Y/%m', blank=True, null=True, verbose_name='Фото')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


