from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    ExtraDescription,
    Description,
    ExtraDescImage,
    Blog,

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


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['id', 'title', 'video', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductListSerializer(serializers.ModelSerializer):
    product_description = ExtraDescriptionSerializer()
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'price', 'product_images', 'product_video', 'product_description']


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