from django.db import models
from django.utils.html import mark_safe

from account.models import User
from .product import Product


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    
    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    def total_price(self):
        return sum([item.total_price for item in self.order_products.all()])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='a')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return ''

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.product.product_images.all().first().image.url))
    image_tag.short_description = 'Image'

    @property
    def total_price(self):
        return sum([item.subtotal for item in self.order_items.all()]) + self.subtotal

    @property
    def subtotal(self):
        return self.price * self.quantity


class OrderProductItem(models.Model):
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    quantity = models.PositiveIntegerField(default=1)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" />'%(self.product.product_images.all().first().image.url))
    image_tag.short_description = 'Image'

    @property
    def subtotal(self):
        return self.price * self.quantity