# Generated by Django 4.2.4 on 2023-08-11 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_productvideo_description_productvideo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvideo',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_video', to='shop.product'),
        ),
    ]