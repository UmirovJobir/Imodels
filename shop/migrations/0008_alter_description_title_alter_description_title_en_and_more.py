# Generated by Django 4.2.4 on 2023-12-11 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_description_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='description',
            name='title_en',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='description',
            name='title_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='description',
            name='title_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif sarlavhasi'),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='title_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='title_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='title_uz',
            field=models.TextField(blank=True, null=True),
        ),
    ]
