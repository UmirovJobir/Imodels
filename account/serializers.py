from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'first_name', 'last_name']
    
