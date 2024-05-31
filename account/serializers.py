from rest_framework import serializers

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import time

from libs.sms import client
from libs.telegram import send_message
from .utils import generate_code
from .models import User, AuthSms
from .validators import phone_regex, is_valid_password


class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(is_active=False, **validated_data)

        auth_sms = AuthSms.objects.create(user=user, secure_code=generate_code())
    
        return user


class UserSerializer(serializers.ModelSerializer):
    secure_code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name', 'secure_code']
        extra_kwargs = {
            'secure_code': {'write_only': True}
        }
    
    @transaction.atomic
    def update(self, instance, validated_data):
        secure_code = validated_data.pop('secure_code', None)
        if 'phone' in validated_data and instance.phone != validated_data['phone']:
            if secure_code is None:
                raise serializers.ValidationError({"secure_code": "This field is required for phone number update."})

            auth_sms = instance.new_phone.last()
            print(auth_sms.phone)
            if auth_sms.secure_code != secure_code:
                            return Response({"error": AuthSms.INVALID_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)
            
            time_difference = timezone.now() - auth_sms.created_at
            if time_difference.total_seconds() > 120:
                return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(instance, validated_data)
    

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
        if not is_valid_password(password):
            raise serializers.ValidationError(User.INVALID_PASSWORD)
        
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("token or encoded_pk is not given")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = get_object_or_404(User, pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.is_active=True
        user.save()
        return data