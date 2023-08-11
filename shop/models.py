from django.db import models

from tinymce import models as tinymce_models


class Category(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
    
    def __str__(self) -> str:
        return f"(Category_pk:{self.pk}, name:{self.name})"


class Product(models.Model):
    title       = models.CharField(max_length=200)
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    description = tinymce_models.HTMLField()

    def __str__(self) -> str:
        return f"(Product_pk:{self.pk}, title:{self.title})"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImage(models.Model):
    image   = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

    def __str__(self) -> str:
        return f"(ProductImage_pk:{self.pk}, product:{self.product.title})"