# Generated by Django 4.2.4 on 2023-09-05 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_configuratorproduct_configurator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurator',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='configurators', to='shop.product'),
            preserve_default=False,
        ),
    ]