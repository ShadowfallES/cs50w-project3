# Generated by Django 3.2.9 on 2021-12-16 23:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='creado',
            field=models.DateField(default=datetime.datetime(2021, 12, 16, 17, 14, 48, 10688)),
        ),
    ]