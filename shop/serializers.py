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
    DescriptionImage,
    ProductFeature,
    ProductFeaturePoint,
    Blog,
    ContactRequest,
    Type,
    Item,
    Order,
    OrderProduct,
    OrderProductItem,
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

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']
    
    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title

    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)
    
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
    type = serializers.SerializerMethodField('get_type')

    class Meta:
        model = Item
        fields = ['type', 'product']
    
    def get_type(self, obj):
        try:
            type_name = obj.type.name
        except AttributeError:
            type_name = None
        
        return type_name
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_data = data.pop('product', None)
        if product_data:
            data.update(product_data)
        return data


# Serializers related to Extra Description
class DescriptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionImage
        fields = ['id', 'image']


class DescriptionPointSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField('get_text')

    class Meta:
        model = DescriptionPoint
        fields = ['id', 'text']

    def get_text(self, obj):
        text = get_full_value(obj=obj, field='text')
        return text


class DescriptionSerializer(serializers.ModelSerializer):
    description_images = DescriptionImageSerializer(many=True)
    description_points = DescriptionPointSerializer(many=True)
    title = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Description
        fields = ['id', 'title', 'description_images', 'description_points',]

    def get_title(self, obj):
        title = get_full_value(obj=obj, field='title')
        return title

# Serializers related to Product
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
    product_features = ProductFeatureSerializer()
    product_description = DescriptionSerializer()
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()
    items = ItemSerializer(many=True)
    price = serializers.SerializerMethodField('get_price')
    title = serializers.SerializerMethodField('get_title')
    information = serializers.SerializerMethodField('get_information')

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'information', 
                  'price', 'configurator', 'items', 'product_images', 'product_video', 
                  'product_description', 'product_features'
                ]
    
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


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')
    price = serializers.SerializerMethodField('get_price')
    title = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'image', 'price']

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


# Serializers related to Order
class OrderProductItemSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductItem
        fields = ['product', 'price', 'quantity']


class OrderProductSerializer(serializers.ModelSerializer):
    order_items = OrderProductItemSerilaizer(many=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'price', 'quantity', 'order_items']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_products']
    
    @transaction.atomic
    def create(self, validated_data):
        order_instance = Order.objects.create(customer=validated_data['customer'])
        order_products_data = validated_data.pop('order_products')

        for order_product_data in order_products_data:
            order_items_data = order_product_data.pop('order_items')

            order_product, created = OrderProduct.objects.get_or_create(order = order_instance, **order_product_data)
            if created==False:
                order_product.price += order_product_data.get('price')
                order_product.quantity += order_product_data.get('quantity')
                order_product.save()

            for order_item_data in order_items_data:
                order_product_item, created = OrderProductItem.objects.get_or_create(order_product = order_product, **order_item_data)
                if created==False:
                    order_product_item.price += order_item_data.get('price')
                    order_product_item.quantity += order_product_item.get('quantity')
                    order_product_item.save()
        
        cart = Cart(self.context.get('request'))
        cart.clear()

        return order_instance
    

# Serializers related to Cart
class CartItemSerilaizer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        fields = ['id', 'quantity']


class CartProductSerilaizer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    items = CartItemSerilaizer(many=True, required=False, allow_null=True)

    class Meta:
        fields = ['id', 'quantity', "items"]

    # def validate(self, data):
    #     id = data.get('id')
    #     quantity = data.get('quantity')
    #     items = data.get('items')
        
    #     print
    #     if items==None and quantity < 1:
    #         raise serializers.ValidationError("field1 cannot be greater than field2")

