# Generated by Django 3.2.6 on 2021-08-17 15:27

import app.models
import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20210817_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='user_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(blank=True, default=None, null=True), default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='promo',
            name='promo_id',
            field=models.CharField(default=app.models.get_code, max_length=255, unique=True, verbose_name='Промокод'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='valid_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 17, 20, 27, 53, 211845), verbose_name='Действителен до'),
        ),
    ]
