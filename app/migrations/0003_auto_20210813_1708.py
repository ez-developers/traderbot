# Generated by Django 3.2.6 on 2021-08-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210813_1205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата присоединения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Телефон'),
        ),
    ]