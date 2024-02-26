# Generated by Django 4.2.4 on 2023-12-06 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='description',
            name='product',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, related_name='product_description', to='shop.product'),
            preserve_default=False,
        ),
    ]