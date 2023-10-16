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
    main_item = serializers.SerializerMethodField('get_main_item')
    items = serializers.SerializerMethodField('get_items')
    price = serializers.SerializerMethodField('get_price')
    title = serializers.SerializerMethodField('get_title')
    information = serializers.SerializerMethodField('get_information')

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'information', 
                  'price', 'configurator', 'main_item','items', 'product_images', 'product_video', 
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
        fields = ['product', 'price', 'price_usd', 'price_eur', 'quantity']


class OrderProductSerializer(serializers.ModelSerializer):
    order_items = OrderProductItemSerilaizer(many=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'price', 'price_usd', 'price_eur', 'quantity', 'order_items']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_products']
    
    @transaction.atomic
    def create(self, validated_data):
        order_instance = Order.objects.create(customer=validated_data['customer'])
        order_products = validated_data.pop('order_products')

        # print(validated_data)

        # for order_product in order_products:
        #     order_items_data = order_product.pop('order_items')

        #     order_product, created = OrderProduct.objects.get_or_create(order = order_instance, **order_product)
        #     if created==False:
        #         order_product.price += order_product.get('price')
        #         order_product.quantity += order_product.get('quantity')
        #         order_product.save()

        #     for order_item_data in order_items_data:
        #         order_product_item, created = OrderProductItem.objects.get_or_create(order_product = order_product, **order_item_data)
        #         if created==False:
        #             order_product_item.price += order_item_data.get('price')
        #             order_product_item.quantity += order_product_item.get('quantity')
        #             order_product_item.save()

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

