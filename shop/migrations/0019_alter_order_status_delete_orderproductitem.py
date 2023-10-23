# Generated by Django 4.2.4 on 2023-10-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', "To'langan"), ('pending', 'Kutish'), ('rejected', 'Rad etilgan')], default='pending', max_length=50),
        ),
        migrations.DeleteModel(
            name='OrderProductItem',
        ),
    ]