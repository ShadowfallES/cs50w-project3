# Generated by Django 3.2.9 on 2021-12-17 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_alter_cartitems_l_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='l_extra',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Extras'),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='t_lista',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Toppings'),
        ),
    ]
