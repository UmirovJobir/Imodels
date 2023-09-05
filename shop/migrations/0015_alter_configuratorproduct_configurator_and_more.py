# Generated by Django 4.2.4 on 2023-09-05 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_configurator_configuratorproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuratorproduct',
            name='configurator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='configurator_title', to='shop.configurator'),
        ),
        migrations.AlterField(
            model_name='configuratorproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configurator_product', to='shop.product'),
        ),
    ]
