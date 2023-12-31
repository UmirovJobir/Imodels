from django.db import models

from .product import Product

def product_extradesc_image_directory_path(instance: "Description", filename: str) -> str:
    return "product_description/product_{pk}__{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Description(models.Model):
    title = models.TextField(null=True, blank=True, verbose_name="Tavsif sarlavhasi")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Qo'shimcha tavsif"
        verbose_name_plural = "Qo'shimcha tavsiflar"


class DescriptionPoint(models.Model):
    text = models.TextField()
    description = models.ForeignKey(Description, on_delete=models.CASCADE, related_name='description_points')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
