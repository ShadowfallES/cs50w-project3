# Generated by Django 3.2.9 on 2021-12-17 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20211216_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='creado',
            field=models.DateField(default=datetime.datetime(2021, 12, 17, 0, 2, 15, 620023)),
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='t_lista',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='t_lista',
            field=models.ManyToManyField(blank=True, max_length=50, null=True, to='orders.Topping'),
        ),
    ]
