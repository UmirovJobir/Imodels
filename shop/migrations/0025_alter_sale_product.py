# Generated by Django 4.2.4 on 2023-11-02 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_sale', to='shop.product'),
        ),
    ]
