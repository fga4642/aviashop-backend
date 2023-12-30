from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class Spare(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, default="Название авиазапчасти", verbose_name="Название")
    status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="Статус")
    image = models.ImageField(upload_to="spares", default="spares/default.jpg", verbose_name="Фото")
    description = models.TextField(max_length=500, default='Описание авиазапчасти', verbose_name="Описание")
    price = models.IntegerField(default=1000, verbose_name="Цена")
    weight = models.FloatField(default=10.0, verbose_name="Вес")
    rating = models.FloatField(default=4.5, verbose_name="Рейтинг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Авиазапчасть"
        verbose_name_plural = "Авиазапчасти"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="Статус", db_index=True)
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Покупатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Администратор", related_name='moderator', blank=True, null=True)

    spares = models.ManyToManyField(Spare, verbose_name="Авиазапчасти", null=False)

    delivery_date = models.IntegerField(default=-1, verbose_name="Дата доставки")

    def __str__(self):
        return "Заказ №" + str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('-date_of_formation', )
