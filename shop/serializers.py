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
    preview_image = serializers.SerializerMethodField('get_product_preview_image')
    product_images = ProductImageSerializer(many=True)
    product_video = ProductVideoSerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'price', 'preview_image', 'product_images', 'product_video']
    
    def get_product_preview_image(self, obj):
        return obj.product_images.first().image.url


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

