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
    ConfiguratorCategory,
)


# Serializers related to Configurator
class ConfiguratorProductNotPriceSerializer(serializers.ModelSerializer):  #Serializer for ConfiguratorListAPI to send data without price
    image = serializers.SerializerMethodField('get_first_image')

    class Meta:
        model = Product
        fields = ['id', 'title', 'image']
    
    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)


class ConfiguratorProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_first_image')

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image']
    
    def get_first_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.product_images.all().first().image.url)


class ConfiguratorCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_products')
    
    class Meta:
        model = ConfiguratorCategory
        fields = ['id', 'name', 'products']

    def get_products(self, obj):
        products = ConfiguratorProductSerializer(
                            [conf_product.product for conf_product in obj.products.all()], 
                            many=True, context={'request': self.context['request']})
        return products.data


class ConfiguratorSerializer(serializers.ModelSerializer):
    conf_category = ConfiguratorCategorySerializer(many=True)
    
    class Meta:
        model = Configurator
        fields = ['id', 'conf_title', 'conf_image', 'conf_category']



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
    configurator = ConfiguratorSerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 
                  'price', 'related_configurator', 'configurator', 'product_images', 'product_video', 
                  'product_description', 'product_features'
                ]


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

