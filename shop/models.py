from django.db import models

from tinymce import models as tinymce_models


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_category', null=True, blank=True)
    name = models.JSONField()
    
    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'
    
    def __str__(self) -> str:
        return f"(Category_pk:{self.pk}, name:{self.name})"


class Product(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    title       = models.CharField(max_length=200)
    description = tinymce_models.HTMLField()
    price       = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self) -> str:
        return f"(Product_pk:{self.pk}, title:{self.title})"
    
    