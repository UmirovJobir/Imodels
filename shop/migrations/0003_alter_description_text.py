# Generated by Django 4.2.4 on 2023-09-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='text',
            field=models.TextField(),
        ),
    ]
