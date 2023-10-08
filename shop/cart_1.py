from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from .serializers import ProductListSerializer
from .models import Product


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def save(self):
        self.session.modified = True


    def add(self, product, items:list=[], quantity=1, overide_quantity=False):
        """
        Add product to the cart or update its quantity
        """
        product = get_object_or_404(Product, pk=product)

        items_data = {}
        if len(items)!=0:
            for item in items:
                product_item = get_object_or_404(Product, pk=item["product"])
                items_data[str(product_item.pk)] = {"quantity": item["quantity"]}
        
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "items": items_data
            }

        if overide_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            product_count = self.cart[product_id]["quantity"]

            self.cart[product_id]["quantity"] += quantity

            if product_count > 0:
                for item in self.cart[product_id]["items"].values():
                    item["quantity"] *= self.cart[product_id]["quantity"]
            
        self.save()


    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            return True
        else:
            return False


    def __iter__(self, request):
        """
        Loop through cart items and fetch the products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            serializer = ProductListSerializer(product, context={'request': request})
            cart[str(product.id)]["product"] = serializer.data
            cart[str(product.id)]["price"] = product.price

        for item in cart.values():
            json = {}
            if item["product"]["price"]:
                for key, value in item["product"]["price"].items():
                    json[key] = value *  item["quantity"]
                    item["subtotal_price"] = json
                item.pop("price")
                yield item
            else:
                item["subtotal_price"] = json
                item.pop('price')
                yield item



    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())


    def get_total_price(self):
        prices = [item["subtotal_price"] for item in self.cart.values()]
        json = {}
        for price in prices:
            for key, value in price.items():
                if key in json:
                    json[key] += value
                else:
                    json[key] = value
        return json


    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
