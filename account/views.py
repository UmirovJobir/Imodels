from rest_framework.response import Response
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from libs.telegram import telebot
from .utils import generate_code
from .models import User, AuthSms
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    PhoneRequestSerializer,
    ResetPasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class VerifyView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, phone=request.data.get('phone'))
        auth_sms = user.authsms

        if auth_sms.secure_code != request.data.get('secure_code'):
            return Response({"error": AuthSms.WRONG_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - auth_sms.created_at
        if time_difference.total_seconds() > 120:
            return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active=True
            user.save()
            return Response({"detail": AuthSms.USER_ACTIVETED}, status=status.HTTP_202_ACCEPTED)


class ResendView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, phone=request.data.get('phone'))

        auth_sms = user.authsms
        auth_sms.secure_code = generate_code()
        auth_sms.created_at = timezone.now()
        auth_sms.save()

        telebot.send_message(text = AuthSms.AUTH_VERIFY_CODE_TEXT.format(auth_sms.secure_code), _type='chat_id_orders')

        return Response({"detail": AuthSms.SECURE_CODE_RESENT}, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class PasswordResetTokenAPI(generics.GenericAPIView):
    serializer_class = PhoneRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, phone=serializer.data["phone"])
        auth_sms = user.authsms

        if auth_sms.secure_code == serializer.data['secure_code']:
            time_difference = timezone.now() - auth_sms.created_at
            if time_difference.total_seconds() > 120:
                return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({"error": AuthSms.WRONG_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)
        

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        return Response({"token": f"{encoded_pk}/{token}"}, status=status.HTTP_200_OK)


class ResetPasswordAPI(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        return Response({"detail": User.PASSWORD_REST}, status=status.HTTP_200_OK)

