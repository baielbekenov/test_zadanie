from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, verbose_name='Название')
    created_at = models.CharField(max_length=150, unique=True, null=True, verbose_name='Дата создание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


