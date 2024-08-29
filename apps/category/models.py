from django.db import models


class AppBar(models.Model):
    image = models.ImageField(upload_to='images/appbar/%Y/%m', blank=True, null=True, verbose_name='АппБар')

    class Meta:
        verbose_name = 'Аппбар'
        verbose_name_plural = 'Аппбар'


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, verbose_name='Название')
    image = models.ImageField(upload_to='images/category/%Y/%m', blank=True, null=True, verbose_name='Фото')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


