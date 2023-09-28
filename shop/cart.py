from django.conf import settings
from decimal import Decimal
from .models import Product
from . import api

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart


    def add(self, product, quantity=1, items:list=[], override_quantity=True):
        product_id = product.id
        if product_id not in self.cart:
            data = {}
            if len(items)==0:
                data['id'] = product_id
                data['quantity'] = quantity
                self.cart.append(data)
            else:
                data['id'] = product_id
                data['quantity'] = quantity
                data['items'] = items
                self.cart.append(data)
        self.save()


    def save(self):
        self.session.modified = True

    def remove(self, product):
        if product.id in [item['id'] for item in self.cart]:
            for item in self.cart:
                if item['id']==product.id:
                    self.cart.remove(item)
            self.save


    # def __iter__(self, request):
    #     currency = request.META.get('HTTP_CURRENCY', 'usd')

    #     product_list = []
    #     total_cost = 0

    #     product_ids = [id['id'] for id in self.cart]

    #     products = Product.objects.filter(id__in=product_ids).select_related('category', 'related_product')
    #     cart = self.cart.copy()
    #     for product in products:
    #         serializer = ProductListSerializer(product, context={'request': request}).data
    #         print(serializer)

        # for product in products:
        #     cart["test"] = ProductListSerializer(product, context={'request': request}).data
        #     print(cart)
        # for item in cart.values():
        #     item["price"] = Decimal(item["price"]) 
        #     item["total_price"] = item["price"] * item["quantity"]
        #     yield item
        # yield "a"
    

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()