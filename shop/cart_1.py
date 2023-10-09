from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from .serializers import ProductListSerializer
from .models import Product

from pprint import pprint

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
        
        product_id = str(product.pk)
        if product_id not in self.cart:
            items_data = {}
            if len(items)!=0:
                for item in items:
                    product_item = get_object_or_404(Product, pk=item["product"])
                    items_data[str(product_item.pk)] = {"quantity": item["quantity"]}

            self.cart[product_id] = {
                "quantity": 0,
            }
            self.cart[product_id]["items"] = items_data
        
        if overide_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            # product_count = self.cart[product_id]["quantity"]

            self.cart[product_id]["quantity"] += quantity

            # if product_count > 0:
            #     for item in self.cart[product_id]["items"].values():
            #         item["quantity"] *= self.cart[product_id]["quantity"]
            
        self.save()


    def remove(self, product):
        """
        Remove a product from the cart
        """
        # product_id = str(product)
        # if product_id in self.cart:
        #     del self.cart[product_id]
        #     self.save()
        #     return True
        # else:
        #     return False
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()



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

        for product in cart.values():
            if product["items"]:
                item_list = []
                
                for item_id, value in product["items"].items():
                    item = get_object_or_404(Product, id=item_id)
                    serializer = ProductListSerializer(item, context={'request': request})
                    serialized_data_dict = dict(serializer.data)
                    serialized_data_dict["quantity"] = value["quantity"] * product["quantity"]

                    item_subtotal_price = {}
                    for price_key, price_value in serialized_data_dict["price"].items():
                        item_subtotal_price[price_key] = price_value *  value["quantity"]
                        serialized_data_dict["subtotal_price"] = item_subtotal_price

                    item_list.append(serialized_data_dict)

                product["product"]["items"] = item_list

            product_subtotal_price = {}
            if product["product"]["price"]:
                for key, value in product["product"]["price"].items():
                    product_subtotal_price[key] = value *  product["quantity"]
                    product["subtotal_price"] = product_subtotal_price
                
                product.pop("price")
                product.pop("items")
                yield product
            else:
                product["subtotal_price"] = None
                product.pop('price')
                product.pop("items")
                yield product



    # def __len__(self):
    #     """
    #     Count all items in the cart
    #     """
    #     return sum(item["quantity"] for item in self.cart.values())


    def get_total_price(self, data):
        prices = []

        for product in data:
            if product["subtotal_price"]:
                    prices.append(product["subtotal_price"])

            if "items" in product["product"]: 
                for item_price in product["product"]["items"]:
                    prices.append(item_price["subtotal_price"])

        total_usd = 0
        total_eur = 0
        total_uzs = 0

        for group_data in prices:
            total_usd += group_data["usd"]
            total_eur += group_data["eur"]
            total_uzs += group_data["uzs"]

        sum = {
            "usd": total_usd,
            "eur": total_eur,
            "uzs": total_uzs
        }          
        return sum


    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
