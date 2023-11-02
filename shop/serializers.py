from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404
from .translation import get_full_value
# from account.serializers import UserSerializer
from . import api
# from .cart import Cart
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    Description,
    DescriptionPoint,
    ProductFeature,
    ProductFeaturePoint,
    ProductGallery,
    Blog,
    ContactRequest,
    Type,
    Item,
    Order,
    OrderProduct,
    Sale
)


# Serializers related to Category
class SubCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_product_count')
    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Category
        fields = ['id', 'name', 'count']
    
    def get_product_count(self, obj):
        count = obj.products.all().count()
        if count==0:
            products = [subcategory.products.all().count() for subcategory in obj.subcategories.all()]
            count = sum(products)
        return count

    def get_name(self, obj):
        name = get_full_value(obj=obj, field='name')
        return name


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField('get_subcategories')
    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
    
    def get_subcategories(self, obj):
        serializer = SubCategorySerializer(obj.subcategories.all(), many=True)
        return serializer.data
    
    def get_name(self, obj):
        name = get_full_value(obj=obj, field='name')
        return name


# Serializers related to Configurator
class ItemDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')
    image = serializers.SerializerMethodField('get_first_image')
    price = serializers.SerializerMethodField('get_price')
    new_price = serializers.SerializerMethodField('get_new_price')
    discount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'new_price', 'discount', 'image']
    
    def get_discount(self, obj):
        try:
            discount = obj.product_sale.discount
        except Sale.DoesNotExist:
            discount = None
        return discount

    def get_new_price(self, obj):
        try:
            new_price = api.get_currency(obj.product_sale.new_price)
        except Sale.DoesNotExist:
            new_price = None
        return new_price


    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title

    def get_first_image(self, obj):
        first_image = obj.product_images.first()
        if first_image:
            return self.context['request'].build_absolute_uri(first_image.image.url)
        else:
            return None

    def get_price(self, obj):
        if obj.price:
            price = api.get_currency(obj_price=obj.price)
        else:
            price = obj.price
        return price


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    product = ItemDetailSerializer()

    class Meta:
        model = Item
        fields = ['product']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data['product']


# Serializers related to Extra Description
class DescriptionPointSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField('get_text')

    class Meta:
        model = DescriptionPoint
        fields = ['id', 'text']

    def get_text(self, obj):
        text = get_full_value(obj=obj, field='text')
        return text


class DescriptionSerializer(serializers.ModelSerializer):
    description_points = DescriptionPointSerializer(many=True)
    title = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Description
        fields = ['id', 'title', 'description_points',]

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title

# Serializers related to Product
class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['id', 'image']

class ProductFeaturePointSerializer(serializers.ModelSerializer):
    feature = serializers.SerializerMethodField('get_feature')

    class Meta:
        model = ProductFeaturePoint
        fields = ['id', 'feature']
    
    def get_feature(self, obj):
        feature = get_full_value(obj=obj, field='feature')
        return feature


class ProductFeatureSerializer(serializers.ModelSerializer):
   features = ProductFeaturePointSerializer(many=True)

   class Meta:
        model = ProductFeature
        fields = ['id', 'image', 'features']


class ProductVideoSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')
    text = serializers.SerializerMethodField('get_text')

    class Meta:
        model = ProductVideo
        fields = ['id', 'title', 'text', 'video_link']

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title
    
    def get_text(self, obj):
        text = get_full_value(obj=obj, field='text')
        return text


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()
    product_features = ProductFeatureSerializer()
    product_galleries = ProductGallerySerializer(many=True)
    product_description = DescriptionSerializer()

    main_item = serializers.SerializerMethodField('get_main_item')
    items = serializers.SerializerMethodField('get_items')
    price = serializers.SerializerMethodField('get_price')
    title = serializers.SerializerMethodField('get_title')
    information = serializers.SerializerMethodField('get_information')
    new_price = serializers.SerializerMethodField('get_new_price')
    discount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Product
        fields = ['id', 'category', 'is_configurator', 'configurator', 'price', 'new_price', 'discount',
                  'title', 'information', 'main_item','items', 'product_images', 'product_video', 
                  'product_galleries', 'product_description', 'product_features'
                ]

    def get_discount(self, obj):
        try:
            discount = obj.product_sale.discount
        except Sale.DoesNotExist:
            discount = None
        return discount

    def get_new_price(self, obj):
        try:
            new_price = api.get_currency(obj.product_sale.new_price)
        except Sale.DoesNotExist:
            new_price = None
        return new_price

    def get_price(self, obj):
        if obj.price:
            price = api.get_currency(obj_price=obj.price)
        else:
            price = obj.price
        return price

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title

    def get_information(self, obj):
        description = get_full_value(obj=obj, field='information')
        return description
    
    def get_main_item(self, obj):
        request = self.context.get('request')
        item = Item.objects.filter(item=obj, type__isnull=True).select_related('type').first()
        if item:
            item_serializer = ItemDetailSerializer(item.product, context={'request': request})
            return item_serializer.data
        else:
            return None

    def get_items(self, obj):
        items = Item.objects.filter(item=obj, type__isnull=False).select_related('type')
        type_names = items.values_list('type__name', flat=True).distinct()

        request = self.context.get('request')

        type_data = []
        for type_name in type_names:
            type_items = items.filter(type__name=type_name)
            item_serializer = ItemSerializer(type_items, many=True, context={'request': request})
            type_data.append({
                'type': type_name,
                'product': item_serializer.data
            })
        
        if type_data:
            return type_data
        else:
            return None


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')
    price = serializers.SerializerMethodField('get_price')
    new_price = serializers.SerializerMethodField('get_new_price')
    discount = serializers.SerializerMethodField('get_discount')
    title = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Product
        fields = ['id', 'order_by', 'category', 'title', 'image', 'price', 'new_price', 'discount']

    def get_discount(self, obj):
        try:
            discount = obj.product_sale.discount
        except Sale.DoesNotExist:
            discount = None
        return discount

    def get_new_price(self, obj):
        try:
            new_price = api.get_currency(obj.product_sale.new_price)
        except Sale.DoesNotExist:
            new_price = None
        return new_price

    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)

    def get_price(self, obj):
        if obj.price:
            price = api.get_currency(obj_price=obj.price)
        else:
            price = obj.price
        return price

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title


# Serializers related to Blog
class BlogListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')
    description = serializers.SerializerMethodField('get_description')

    class Meta:
        model = Blog
        fields = ['id', 'preview_image', 'title', 'description', 'created_at']

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title
    
    def get_description(self, obj):
        description = get_full_value(obj=obj, field='description')
        return description
    

class BlogDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField('get_title')
    description = serializers.SerializerMethodField('get_description')
    text = serializers.SerializerMethodField('get_text')

    class Meta:
        model = Blog
        fields = ['id', 'preview_image', 'title', 'description', 'text', 'created_at']

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title
    
    def get_description(self, obj):
        description = get_full_value(obj=obj, field='description')
        return description
    
    def get_text(self, obj):
        text = get_full_value(obj=obj, field='text')
        return text


# Serializers related to ContactRequest
class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'email', 'phone', 'message']


class OrderProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')
    title = serializers.SerializerMethodField('get_title')
    quantity = serializers.SerializerMethodField('get_quantity')
    price = serializers.SerializerMethodField('get_price')
    configurator = serializers.SerializerMethodField('get_configurator')

    class Meta:
        model = Product
        fields = ['id', 'configurator', 'title', 'image', 'quantity', 'price']

    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title

    def get_quantity(self, obj):
        return self.context.get('request').data['quantity']

    def get_price(self, obj):
        return self.context.get('request').data['price']
    
    def get_configurator(self, obj):
        return self.context.get('request').data['configurator']


# Serializers related to Order
class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product')

    class Meta:
        model = OrderProduct
        fields = ['product']
    
    def get_product(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            request.data['configurator'] = obj.configurator.pk if obj.configurator else None
            request.data['quantity'] = obj.quantity
            request.data['price'] = {
                "usd": obj.price_usd,
                "uzd": obj.price,
                "eur": obj.price_eur,
            }
        return OrderProductDetailSerializer(
                Product.objects.get(pk=obj.product.pk),
                context = {"request": request}).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data['product']    


class OrderSerializer(serializers.ModelSerializer):
    order_products = serializers.SerializerMethodField('get_order_products')
    created_at = serializers.DateTimeField(required=False, format="%d-%m-%Y %H:%M:%S", input_formats=["%d-%m-%Y %H:%M:%S"])

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'order_products']

    def get_order_products(self, obj):
        request = self.context.get('request')
        order_products = OrderProduct.objects.filter(order=obj.pk)
        return OrderProductSerializer(order_products,
                                        context = {"request": request},
                                        many=True).data


class OrderPriceRequest(serializers.Serializer):
    usd = serializers.DecimalField(decimal_places=2, max_digits=10)
    uzs = serializers.DecimalField(decimal_places=2, max_digits=10)
    eur = serializers.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        fields = ['usd', 'uzs', 'eur']


class OrderRequest(serializers.Serializer):
    configurator = serializers.IntegerField()
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = OrderPriceRequest()

    class Meta:
        fields = ['configurator', 'product', 'quantity', 'price']
    

# Serializers related to Cart
class CartItemRequest(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        fields = ['id', 'quantity']


class CartProductRequest(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    items = CartItemRequest(many=True, required=False, allow_null=True)

    class Meta:
        fields = ['id', 'quantity', "items"]


class SaleSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product')

    class Meta:
        model = Sale
        fields = ['product', 'new_price']

    def get_product(self, obj):
        request = self.context.get('request')
        product_serializer = ProductListSerializer(obj.product, context = {"request": request})
        return product_serializer.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        price = data['product']['price']['usd']
        # discount = round((price - instance.new_price) / price * 100)
                
        data['product']['new_price'] = api.get_currency(instance.new_price)
        data['product']['discount'] = instance.discount
        
        return data['product']