from django.db import models
from django.utils.html import mark_safe

from embed_video.fields import EmbedVideoField

from .category import Category


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    return "product_images/product_{pk}__{filename}".format(
        pk=instance.product.pk,
        filename=filename)

def product_feature_image_directory_path(instance: "ProductFeature", filename: str) -> str:
    return "product_feature/product_{pk}__{filename}".format(
        pk=instance.product.pk,
        filename=filename)

def product_gallery_directory_path(instance: "ProductGallery", filename: str) -> str:
    return "product_gallery/product_{pk}__{filename}".format(
        pk=instance.product.pk,
        filename=filename)


class Product(models.Model):
    STATUS_CHOICES = (
        ('Visible', 'Visible'),
        ('Invisible', 'Invisible'),
    )
    is_configurator = models.BooleanField(default=False)
    configurator = models.ForeignKey('self', on_delete=models.CASCADE, related_name='create_own_set', null=True, blank=True)
    title = models.CharField(max_length=300)
    information = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Visible')
    order_by = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
    
    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    image   = models.ImageField(upload_to=product_image_directory_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'


class ProductVideo(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    video_link = EmbedVideoField(null=True, blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_video')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def video_tag(self):
    #     return f'<iframe width="560" height="315" src="{self.video_link}" frameborder="0" allowfullscreen></iframe>'
    # video_tag.short_description = 'Video'


class ProductFeature(models.Model):
    image   = models.ImageField(upload_to=product_feature_image_directory_path)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_features')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'


class ProductFeaturePoint(models.Model):
    feature = models.CharField(max_length=300)
    product = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name='features')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductGallery(models.Model):
    image = models.ImageField(upload_to=product_gallery_directory_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_galleries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    
    class Meta:
        unique_together = ('product', 'item')

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.product.product_images.first().image.url))
    image_tag.short_description = 'Image'


    def price(self):
        return self.product.price


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sale')
    new_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)