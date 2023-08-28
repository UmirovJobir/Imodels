from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
)


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['id', 'title', 'video', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'price', 'product_images', 'product_video']


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

