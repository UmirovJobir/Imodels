# Generated by Django 4.2.4 on 2023-09-12 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_orderconfigurator_configurator_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderconfigurator',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_configurator', to='shop.orderitem'),
        ),
    ]
