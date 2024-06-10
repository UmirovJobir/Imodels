from rest_framework import serializers

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import time
from datetime import timedelta

from libs.sms import client
from libs.telegram import send_message
from .utils import generate_code
from .models import User
from .validators import phone_regex, is_valid_password


class RegisterSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['id', 'phone', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        secure_code = '111111' if settings.DEBUG else str(random.randint(100000, 999999))
        expiration_time = timezone.now() + timedelta(minutes=1, seconds=30)
        user = User.objects.create(
            phone=validated_data['phone'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            secure_code=secure_code,
            expiration_time=expiration_time,
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()
        # Send confirmation_code via SMS here (integration with SMS gateway needed)
        send_message(
                type='auth',
                text=User.AUTH_VERIFY_CODE_TEXT.format(secure_code))
        
        if settings.DEBUG==False:
            client._send_sms(
                phone=instance.user.phone,
                code=User.AUTH_VERIFY_CODE_TEXT.format(secure_code))
        return user

class ConfirmSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, validators=[phone_regex])
    secure_code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data.get('phone')
        secure_code = data.get('secure_code')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(User.USER_ERROR_MESSAGE)
        
        if user.secure_code != secure_code:
            raise serializers.ValidationError(User.INVALID_SECURE_CODE)

        if user.expiration_time and timezone.now() > user.expiration_time:
            raise serializers.ValidationError(User.SECURE_CODE_EXPIRED)
        
        return data
    
    def save(self):
        phone = self.validated_data['phone']
        user = User.objects.get(phone=phone)
        user.is_active = True
        user.secure_code = None
        user.expiration_time = None
        user.save()
        return user
    
class ResendSecureCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            try:
                user = User.objects.get(new_phone_temp=phone)
            except User.DoesNotExist:
                raise serializers.ValidationError(User.USER_ERROR_MESSAGE)
        return data

    def save(self):
        phone = self.validated_data['phone']
        user = User.objects.get(phone=phone)
        secure_code = '111111' if settings.DEBUG else str(random.randint(100000, 999999))
        expiration_time = timezone.now() + timedelta(minutes=1, seconds=30)
        user.secure_code = secure_code
        user.expiration_time = expiration_time
        user.save()
        # Send confirmation_code via SMS here (integration with SMS gateway needed)
        send_message(
                type='auth',
                text=User.AUTH_VERIFY_CODE_TEXT.format(secure_code))
        
        if settings.DEBUG==False:
            client._send_sms(
                phone=instance.user.phone,
                code=User.AUTH_VERIFY_CODE_TEXT.format(secure_code))
        return user

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    # secure_code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name']
    
    def validate_phone(self, value):
        if self.instance and value != self.instance.phone:
            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError("This phone number is already in use.")
            secure_code = '111111' if settings.DEBUG else str(random.randint(100000, 999999))
            self.instance.secure_code = secure_code
            self.instance.expiration_time = timezone.now() + timedelta(minutes=1, seconds=30)
            self.instance.new_phone_temp = value
            self.instance.save()
            # Send confirmation_code to the new phone number
            send_message(
                type='auth',
                text=User.AUTH_VERIFY_CODE_TEXT.format(secure_code))
        
            if settings.DEBUG==False:
                client._send_sms(
                    phone=instance.user.phone,
                    code=User.AUTH_VERIFY_CODE_TEXT.format(secure_code))
            self.context['secure_code_sent'] = True
        return value

    def update(self, instance, validated_data):
        if 'phone' in validated_data:
            validated_data.pop('phone')  # Remove phone from validated data to prevent direct update

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     secure_code = validated_data.pop('secure_code', None)
    #     if 'phone' in validated_data and instance.phone != validated_data['phone']:
    #         if secure_code is None:
    #             raise serializers.ValidationError({"secure_code": "This field is required for phone number update."})

    #         auth_sms = instance.new_phone.last()
    #         if auth_sms.secure_code != secure_code:
    #                         return Response({"error": AuthSms.INVALID_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)
            
    #         time_difference = timezone.now() - auth_sms.created_at
    #         if time_difference.total_seconds() > 120:
    #             return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)

    #     return super().update(instance, validated_data)
    

class ConfirmPhoneSerializer(serializers.Serializer):
    secure_code = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user
        secure_code = data.get('secure_code')
        
        if user.secure_code != secure_code:
            raise serializers.ValidationError(User.INVALID_SECURE_CODE)
        if user.expiration_time and timezone.now() > user.expiration_time:
            raise serializers.ValidationError(User.SECURE_CODE_EXPIRED)
        
        return data

    def save(self):
        user = self.context['request'].user
        if user.new_phone_temp:
            user.phone = user.new_phone_temp
            user.new_phone_temp = None
        
        user.secure_code = None
        user.expiration_time = None
        user.save()
                                     
        return user


class PhoneResetSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, validators=[phone_regex])

    class Meta:
        field = ["phone"]


class PhoneRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, validators=[phone_regex])
    secure_code = serializers.CharField(max_length=6)
        
    def validate(self, data):
        phone = data.get('phone')
        secure_code = data.get('secure_code')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError(User.USER_ERROR_MESSAGE)
        
        if user.secure_code != secure_code:
            raise serializers.ValidationError(User.INVALID_SECURE_CODE)

        if user.expiration_time and timezone.now() > user.expiration_time:
            raise serializers.ValidationError(User.SECURE_CODE_EXPIRED)
        
        return data


class ResetPasswordSerializer(serializers.Serializer):  
    password = serializers.CharField(write_only=True, min_length=8)

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