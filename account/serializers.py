from rest_framework import serializers

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from libs.telegram import telebot
from .utils import generate_code
from .models import User, AuthSms
from .validators import phone_regex


class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(is_active=False, **validated_data)
        auth_sms = AuthSms.objects.create(user=user, secure_code=generate_code())
        telebot.send_message(text=AuthSms.AUTH_VERIFY_CODE_TEXT.format(auth_sms.secure_code), _type='chat_id_orders')
        return user


class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name']
    

class PhoneResetSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, validators=[phone_regex])

    class Meta:
        field = ["phone"]


class PhoneRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, validators=[phone_regex])
    secure_code = serializers.CharField(max_length=6)

    class Meta:
        field = ["phone", "secure_code"]


class ResetPasswordSerializer(serializers.Serializer):  
    password = serializers.CharField(write_only=True, min_length=1)

    class Meta:
        field = ["password"]

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("token or encoded_pk is not given")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = get_object_or_404(User, pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data