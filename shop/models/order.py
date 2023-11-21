from django.db import models
from django.utils.html import mark_safe

from account.models import User
from .product import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("Kutish", "Kutish"),
        ("To'langan", "To'langan"),
        ("Rad etilgan", "Rad etilgan"),
    )
    PAYMENT_CHOICES = (
        ("Naqd", "Naqd"),
        ("Payme", "Payme"),
    )
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default=PAYMENT_CHOICES[0][1])
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][1])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    @property
    def total_price(self):
        return sum([item.subtotal for item in self.order_products.all()])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_usd = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_eur = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    configurator = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_configurator', null=True, blank=True)

    def image_tag(self):
        try:
            first_image = self.product.product_images.first().image.url
        except AttributeError:
            first_image = "/static/img/no-image.png"
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(first_image))
    image_tag.short_description = 'Image'

    @property
    def product_name(self):
        return self.product.title

    @property
    def subtotal(self):
        return self.price * self.quantity if self.price!=None else 0


