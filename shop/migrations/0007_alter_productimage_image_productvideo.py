# Generated by Django 4.2.4 on 2023-08-11 11:04

from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=shop.models.product_image_directory_path),
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to=shop.models.product_video_directory_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_video', to='shop.product')),
            ],
        ),
    ]
