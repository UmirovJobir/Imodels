from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from tinymce import models as tinymce_models
from .validators import validate_phone_length


def configurator_image_directory_path(instance: "Configurator", filename: str) -> str:
    return "configurator_image/configurator_{pk}__{filename}".format(
        pk=instance.pk,
        filename=filename
    )

def blog_image_directory_path(instance: "Blog", filename: str) -> str:
    return "blog_images/blog_{pk}__{filename}".format(
        pk=instance.pk,
        filename=filename
    )

def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    return "product_images/product_{pk}__{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )

def product_video_directory_path(instance: "ProductVideo", filename: str) -> str:
    return "product_video/product_{pk}__{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )

def product_extradesc_image_directory_path(instance: "ExtraDescription", filename: str) -> str:
    return "product_extradesc/product_{pk}__{filename}".format(
        pk=instance.extra_desc.pk,
        filename=filename
    )

def product_feature_image_directory_path(instance: "ProductFeature", filename: str) -> str:
    return "product_feature/product_{pk}__{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )


class Category(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
    
    def __str__(self) -> str:
        return f"(Category_pk:{self.pk}, name:{self.name})"


class Product(models.Model):
    related_configurator = models.ForeignKey('self', on_delete=models.CASCADE, related_name='create_own_set', null=True, blank=True)
    title = models.CharField(max_length=300)
    description = tinymce_models.HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(Product_pk:{self.pk}, title:{self.title})"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def image_tag(self):
        first_image = self.product_images.all().first().image.url
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(first_image))
    image_tag.short_description = 'Image'


class ProductImage(models.Model):
    image   = models.ImageField(upload_to=product_image_directory_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ProductImage_pk:{self.pk}, product:{self.product.title})"
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'


class ProductVideo(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    description = tinymce_models.HTMLField(null=True, blank=True)
    video = models.FileField(upload_to=product_video_directory_path)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_video')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ProductVideo_pk:{self.pk}, product:{self.product.title})"
    
    def video_tag(self):
        return '<source src="%s" type="video/mp4">'%(self.video.url)
    video_tag.short_description = 'Video'


class ExtraDescription(models.Model):
    title = models.CharField(max_length=500)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ExtraDescription_pk:{self.pk}, product:{self.product.title})"


class Description(models.Model):
    text = tinymce_models.HTMLField()
    extradescription = models.ForeignKey(ExtraDescription, on_delete=models.CASCADE, related_name='extradescription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(Description_pk:{self.pk}, description:{self.extradescription.title})"
    

class ExtraDescImage(models.Model):
    image = models.ImageField(upload_to=product_extradesc_image_directory_path)
    extra_desc = models.ForeignKey(ExtraDescription, on_delete=models.CASCADE, related_name='extradescription_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ExtraDescImage_pk:{self.pk}, extra_desc:{self.extra_desc.title})"

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'


class ProductFeature(models.Model):
    image   = models.ImageField(upload_to=product_feature_image_directory_path)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_features')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ProductFeatureImage_pk:{self.pk}, product:{self.product.title})"
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.image.url))
    image_tag.short_description = 'Image'


class ProductFeatureOption(models.Model):
    feature = models.CharField(max_length=300)
    product = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name='features')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ProductFeature_pk:{self.pk}, feature:{self.feature})"


class Blog(models.Model):
    preview_image = models.ImageField(upload_to=blog_image_directory_path)
    title = models.CharField(max_length=500)
    text = tinymce_models.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=9, validators=[validate_phone_length])
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Просьба связаться'
        verbose_name_plural = 'Просьбы связаться'


class Configurator(models.Model):
    conf_title = models.CharField(max_length=200)
    conf_image = models.ImageField(upload_to=configurator_image_directory_path, null=True, blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='configurator')

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.conf_image.url))
    image_tag.short_description = 'Image'

    def product_image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.product.product_images.all().first().image.url))
    product_image_tag.short_description = 'Product Image'


class ConfiguratorCategory(models.Model):
    name = models.CharField(max_length=200)
    configurator = models.ForeignKey(Configurator, on_delete=models.PROTECT, related_name='conf_category')


class ConfiguratorProduct(models.Model):
    conf_category = models.ForeignKey(ConfiguratorCategory, on_delete=models.PROTECT, related_name='products')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.product.product_images.all().first().image.url))
    image_tag.short_description = 'Image'
    

class Cart(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the cart to a user
    products = models.ManyToManyField('Product', through='CartItem') 

    @property
    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.subtotal
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

    @property
    def subtotal(self):
        return self.product.price * self.quantity
    

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
#     cart = models.OneToOneField(Cart, on_delete=)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
#     price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
#     quantity = models.PositiveIntegerField(default=1)