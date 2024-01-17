# Generated by Django 4.2.5 on 2024-01-16 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 16, 14, 54, 18, 984685, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.IntegerField(blank=True, null=True, verbose_name='Дата доставки'),
        ),
    ]
