from rest_framework import serializers
from rest_framework.request import Request
from . import api
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    ExtraDescription,
    Description,
    ExtraDescImage,
    ProductFeature,
    ProductFeatureOption,
    Blog,
    ContactRequest,
    Type,
    Item,
    
)


# Serializers related to Configurator
class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']
    
    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)
    
    def get_price(self, obj):
        request = self.context['request']
        currency = request.META.get('HTTP_CURRENCY')
        if currency=='uzs':
            kurs = api.get_usd_currency()
            price = round(obj.price * kurs, 2)
        elif currency=='eur':
            usd = api.get_usd_currency()
            eur = api.get_eur_currency()
            price = round(obj.price * usd / eur, 2)
        elif currency=='usd':
            price = obj.price
        return price


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class ConfiguratorSerializer(serializers.ModelSerializer):
    product = ItemSerializer()
    type = TypeSerializer()

    class Meta:
        model = Item
        fields = ['type', 'product']


# Serializers related to Category
class SubCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_product_count')

    class Meta:
        model = Category
        fields = ['id', 'name', 'count']
    
    def get_product_count(self, obj):
        count = obj.products.all().count()
        if count==0:
            products = [subcategory.products.all().count() for subcategory in obj.subcategories.all()]
            count = sum(products)
        return count


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField('get_subcategories')

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
    
    def get_subcategories(self, obj):
        serializer = SubCategorySerializer(obj.subcategories.all(), many=True)
        return serializer.data


# Serializers related to Extra Description
class ExtraDescImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDescImage
        fields = ['id', 'image']


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'text']


class ExtraDescriptionSerializer(serializers.ModelSerializer):
    extradescription_images = ExtraDescImageSerializer(many=True)
    extradescription = DescriptionSerializer(many=True)

    class Meta:
        model = ExtraDescription
        fields = ['id', 'title', 'extradescription', 'extradescription_images']


# Serializers related to Product
class ProductFeatureOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeatureOption
        fields = ['feature']


class ProductFeatureSerializer(serializers.ModelSerializer):
   features = ProductFeatureOptionSerializer(many=True)

   class Meta:
        model = ProductFeature
        fields = ['id', 'image', 'features']


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['id', 'title', 'video_link', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    product_features = ProductFeatureSerializer()
    product_description = ExtraDescriptionSerializer()
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()
    configurators = ConfiguratorSerializer(many=True)
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 
                  'price', 'related_configurator', 'configurators', 'product_images', 'product_video', 
                  'product_description', 'product_features'
                ]
    
    def get_price(self, obj):
        request = self.context['request']
        currency = request.META.get('HTTP_CURRENCY')
        if currency=='uzs':
            kurs = api.get_usd_currency()
            price = round(obj.price * kurs, 2)
        elif currency=='eur':
            usd = api.get_usd_currency()
            eur = api.get_eur_currency()
            price = round(obj.price * usd / eur, 2)
        elif currency=='usd':
            price = obj.price
        return price


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')
    price = serializers.SerializerMethodField('get_price')

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'image', 'price']

    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)

    def get_price(self, obj):
        request = self.context['request']
        currency = request.META.get('HTTP_CURRENCY')
        if currency=='uzs':
            kurs = api.get_usd_currency()
            price = round(obj.price * kurs, 2)
        elif currency=='eur':
            usd = api.get_usd_currency()
            eur = api.get_eur_currency()
            price = round(obj.price * usd / eur, 2)
        elif currency=='usd':
            price = obj.price
        return price


# Serializers related to Blog
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'preview_image', 'title', 'text']


# Serializers related to ContactRequest
class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'email', 'phone_number', 'message']

