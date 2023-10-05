from django.db import models
from django.utils.html import mark_safe

from .product import Product

def product_extradesc_image_directory_path(instance: "ExtraDescription", filename: str) -> str:
    return "product_extradesc/product_{pk}__{filename}".format(
        pk=instance.extra_desc.pk,
        filename=filename
    )


class ExtraDescription(models.Model):
    title = models.CharField(max_length=500)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Qo'shimcha tavsif"
        verbose_name_plural = "Qo'shimcha tavsiflar"


class Description(models.Model):
    text = models.TextField()
    extradescription = models.ForeignKey(ExtraDescription, on_delete=models.CASCADE, related_name='extradescription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ExtraDescImage(models.Model):
    image = models.ImageField(upload_to=product_extradesc_image_directory_path)
    extra_desc = models.ForeignKey(ExtraDescription, on_delete=models.CASCADE, related_name='extradescription_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'