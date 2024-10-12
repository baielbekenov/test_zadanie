from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone, password=None, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError("The given phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    phone = models.CharField(max_length=15, unique=True, null=False, verbose_name=_('Номер телефона'))
    email = models.EmailField(unique=True, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, verbose_name=_('Код'), blank=True)
    username = models.CharField(unique=False, max_length=250, blank=True, null=True, verbose_name=_('Имя пользователя'))
    last_sms_date = models.DateTimeField(null=True, verbose_name=_('Дата отправки кода'), blank=True)
    is_confirm = models.BooleanField(default=False, blank=True, verbose_name=_('Подтверждение почты'))
    created_at = models.DateField(auto_now_add=True)
    objects = UserManager()
    first_name = None
    last_name = None

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class SingletonModel(models.Model):
    """
    Модель, которая всегда имеет только один экземпляр.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Policy(SingletonModel):
    title = models.CharField(max_length=120, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Политика'
        verbose_name_plural = 'Политика'


class Privacy(SingletonModel):
    title = models.CharField(max_length=120, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Правила'
        verbose_name_plural = 'Правила'