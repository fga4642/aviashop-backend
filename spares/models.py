from django.db import models
from datetime import datetime
from django.utils import timezone
from django.urls import reverse


class Spare(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    CONDITION_CHOICES = (
        (1, 'Новое'),
        (2, 'Б/У'),
    )

    name = models.CharField(max_length=100, default="Название авиазапчасти", verbose_name="Название")
    status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="Статус")
    image = models.ImageField(default="spares/default.jpg", upload_to="spares", verbose_name="Фото")
    description = models.TextField(max_length=500, default='Описание авиазапчасти', verbose_name="Описание")
    price = models.IntegerField(default=1000, verbose_name="Цена")
    weight = models.FloatField(default=10.0, verbose_name="Вес")
    condition = models.IntegerField(default=1, choices=CONDITION_CHOICES, verbose_name="Состояние")
    rating = models.FloatField(default=4.5, verbose_name="Рейтинг")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("order", kwargs={"spare_id": self.pk})

    class Meta:
        verbose_name = "Авиазапчасть"
        verbose_name_plural = "Авиазапчасти"


class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    status = models.IntegerField(default=1, max_length=100, choices=STATUS_CHOICES, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата формирования")
    date_complete = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата завершения")

    spares = models.ManyToManyField(Spare, verbose_name="Авиазапчасти", null=False)

    def __str__(self):
        return "Заказ №" + str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
