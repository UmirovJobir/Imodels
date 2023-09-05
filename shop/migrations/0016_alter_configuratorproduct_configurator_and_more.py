# Generated by Django 4.2.4 on 2023-09-05 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_configuratorproduct_configurator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuratorproduct',
            name='configurator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.configurator'),
        ),
        migrations.AlterField(
            model_name='configuratorproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configurator', to='shop.product'),
        ),
    ]
