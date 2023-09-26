from rest_framework import serializers

from django.db import transaction

from libs.telegram import telebot
from .utils import generate_code
from .models import User, AuthSms


class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(is_active=False, **validated_data)
        auth_sms = AuthSms.objects.create(user=user, secure_code=generate_code())
        telebot.send_message(text=auth_sms.secure_code, _type='chat_id_orders')
        return user


class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name']
    
