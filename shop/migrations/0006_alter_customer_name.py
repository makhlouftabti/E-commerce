# Generated by Django 4.2.6 on 2023-11-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_cart_cartitem_cart_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]