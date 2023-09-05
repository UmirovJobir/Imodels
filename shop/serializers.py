from rest_framework import serializers
from rest_framework.request import Request
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
    Configurator,
    ConfiguratorProduct
)


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
        fields = ['id', 'title', 'video', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductListSerializer(serializers.ModelSerializer):
    product_features = ProductFeatureSerializer()
    product_description = ExtraDescriptionSerializer()
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 
                  'price', 'product_images', 'product_video', 
                  'product_description', 'product_features'
                ]


class SubCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_product_count')

    class Meta:
        model = Category
        fields = ['id', 'name', 'count']
    
    def get_product_count(self, obj):
        return obj.category.all().count()


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField('get_subcategories')

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
    
    def get_subcategories(self, obj):
        serializer = SubCategorySerializer(obj.subcategories.all(), many=True)
        return serializer.data


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'preview_image', 'title', 'text']


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'email', 'phone_number', 'message']


class ConfiguratorProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = ConfiguratorProduct
        fields = ['product']


class ConfiguratorProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']
    
    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)


class ConfiguratorSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_products')
    
    class Meta:
        model = Configurator
        fields = ['id', 'title', 'products']

    def get_products(self, obj):
        products = ConfiguratorProductSerializer(
                            [conf_product.product for conf_product in obj.products.all()], 
                            many=True, context={'request': self.context['request']})
        return products.data


