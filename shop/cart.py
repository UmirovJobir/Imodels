from django.conf import settings
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart


    def add(self, product, quantity=1, configurators:list=[], override_quantity=True):
        product_id = product.id

        if product_id not in self.cart:
            data = {}
            if len(configurators)==0:
                data['id'] = product_id
                data['quantity'] = quantity
                self.cart.append(data)
            else:
                data['id'] = product_id
                data['quantity'] = quantity
                data['configurators'] = configurators
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


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
    

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()