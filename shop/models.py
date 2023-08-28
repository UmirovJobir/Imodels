from django.db import models
from tinymce import models as tinymce_models



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


class Category(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
    
    def __str__(self) -> str:
        return f"(Category_pk:{self.pk}, name:{self.name})"


class Product(models.Model):
    title         = models.TextField(max_length=300)
    description   = tinymce_models.HTMLField()
    category      = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    price         = models.DecimalField(decimal_places=2, max_digits=10, blank=True)

    def __str__(self) -> str:
        return f"(Product_pk:{self.pk}, title:{self.title})"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImage(models.Model):
    image   = models.ImageField(upload_to=product_image_directory_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

    def __str__(self) -> str:
        return f"(ProductImage_pk:{self.pk}, product:{self.product.title})"


class ProductVideo(models.Model):
    title = models.TextField(max_length=500)
    description = tinymce_models.HTMLField()
    video = models.FileField(upload_to=product_video_directory_path)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_video')

    def __str__(self) -> str:
        return f"(ProductVideo_pk:{self.pk}, product:{self.product.title})"


class ExtraDescription(models.Model):
    title = models.TextField(max_length=500)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_description')

    def __str__(self) -> str:
        return f"(ExtraDescription_pk:{self.pk}, product:{self.product.title})"


class Description(models.Model):
    text = models.TextField()
    extradescription = models.ForeignKey(ExtraDescription, on_delete=models.CASCADE, related_name='extradescription')

    def __str__(self) -> str:
        return f"(Description_pk:{self.pk}, description:{self.extradescription.title})"
    

class ExtraDescImage(models.Model):
    image   = models.ImageField(upload_to=product_image_directory_path)
    extra_desc = models.ForeignKey(ExtraDescription, on_delete=models.CASCADE, related_name='extradescription_images')

    def __str__(self) -> str:
        return f"(ExtraDescImage_pk:{self.pk}, extra_desc:{self.extra_desc.title})"