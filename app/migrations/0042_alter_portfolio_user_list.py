# Generated by Django 3.2.6 on 2021-08-19 12:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20210819_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='user_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(default=0), default=list, null=True, size=None),
        ),
    ]
