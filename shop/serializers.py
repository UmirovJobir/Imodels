from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'category', 'title', 'description', 'price'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name'