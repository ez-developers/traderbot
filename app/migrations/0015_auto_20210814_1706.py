# Generated by Django 3.2.6 on 2021-08-14 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210814_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='promo_id',
            field=models.CharField(blank=True, default='UM3NUU', max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='promo',
            name='valid_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 14, 17, 6, 23, 567700)),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(default=None, max_length=2, null=True),
        ),
    ]
