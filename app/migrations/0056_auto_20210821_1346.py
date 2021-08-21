# Generated by Django 3.2.6 on 2021-08-21 08:46

import app.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_auto_20210821_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailings',
            name='date_sent',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки'),
        ),
        migrations.AlterField(
            model_name='mailings',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=app.storage.CustomFileSystemStorage, upload_to='uploads/mailings/%Y_%m_%d/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='mailings',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.portfolio', verbose_name='Портфолио'),
        ),
    ]