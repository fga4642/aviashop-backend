# Generated by Django 4.2.4 on 2023-09-16 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0004_alter_order_date_complete_alter_order_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 16, 17, 6, 4, 736277, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 16, 17, 6, 4, 736277, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 16, 17, 6, 4, 736277, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
        migrations.AlterField(
            model_name='spare',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='spares', verbose_name='Фото'),
        ),
    ]
