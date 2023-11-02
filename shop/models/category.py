from django.db import models


class Category(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name='Kategoriya'
        verbose_name_plural='Kategoriyalar'

    @property
    def product_count(self):
        count = self.products.all().count()
        if count==0:
            products = [subcategory.products.all().count() for subcategory in self.subcategories.all()]
            count = sum(products)
        return count