# Generated by Django 3.2.9 on 2021-12-17 06:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20211217_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='creado',
            field=models.DateField(default=datetime.datetime(2021, 12, 17, 0, 14, 54, 785640)),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='t_lista',
            field=models.ManyToManyField(blank=True, null=True, to='orders.Topping'),
        ),
    ]
