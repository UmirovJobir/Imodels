from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['phone', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name']
    
