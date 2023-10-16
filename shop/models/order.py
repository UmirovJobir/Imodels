from django.db import models
from django.utils.html import mark_safe

from account.models import User
from .product import Product


class Order(models.Model):
    paid = "To'langan"
    pending = "Kutish" 
    STATUS_CHOICES = (
        (paid, "To'langan"),
        (pending, "Kutish"),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=pending)
    
    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    @property
    def total_price(self):
        return sum([item.total_price for item in self.order_products.all()])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_usd = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_eur = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def image_tag(self):
        try:
            first_image = self.product.product_images.first().image.url
        except AttributeError:
            first_image = "/static/img/no-image.png"
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(first_image))
    image_tag.short_description = 'Image'

    @property
    def total_price(self):
        return sum([item.subtotal for item in self.order_items.all()]) + self.subtotal

    @property
    def subtotal(self):
        return self.price * self.quantity if self.price!=None else 0


class OrderProductItem(models.Model):
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_usd = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_eur = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def image_tag(self):
        try:
            first_image = self.product.product_images.first().image.url
        except AttributeError:
            first_image = "/static/img/no-image.png"
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(first_image))
    image_tag.short_description = 'Image'

    @property
    def subtotal(self):
        return self.price * self.quantity if self.price!=None else 0 
