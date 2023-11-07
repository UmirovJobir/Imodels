from rest_framework.response import Response
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from drf_spectacular.utils import extend_schema, OpenApiResponse

from libs.telegram import telebot
from libs.sms import client

from .utils import generate_code
from .models import User, AuthSms
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    PhoneResetSerializer,
    PhoneRequestSerializer,
    ResetPasswordSerializer,
)


@extend_schema(
    tags=["Login"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    tags=["Login"],
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
        tags=["Register"],
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


@extend_schema(
        tags=["Register"],
        request=PhoneRequestSerializer,
        responses={
            200: OpenApiResponse(description="User activated")
        },
)
class ConfirmView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, phone=request.data.get('phone'))
        last_auth_sms = user.authsms.last()

        if last_auth_sms.secure_code != request.data.get('secure_code'):
            return Response({"error": AuthSms.WRONG_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - last_auth_sms.created_at
        if time_difference.total_seconds() > 120:
            return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active=True
            user.save()
            return Response({"detail": AuthSms.USER_ACTIVETED}, status=status.HTTP_202_ACCEPTED)


@extend_schema(
        tags=["Login"],
)
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
        tags=["Password Reset"],
        request=PhoneResetSerializer,
        responses={
            200: OpenApiResponse(description="Created. New resource in response"),
            404: OpenApiResponse(description="Not found"),
        },
)
class ResendView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, phone=request.data.get('phone'))
        
        auth_sms = AuthSms.objects.create(
                    user=user,
                    secure_code = generate_code(),
                    created_at = timezone.now())

        if settings.DEBUG==False:
            client._send_sms(
                phone_number=user.phone,
                message=AuthSms.AUTH_VERIFY_CODE_TEXT.format(auth_sms.secure_code))

        telebot.send_message(
                type='chat_id_orders',
                text=AuthSms.AUTH_VERIFY_CODE_TEXT.format(auth_sms.secure_code))

        return Response({"detail": AuthSms.SECURE_CODE_RESENT}, status=status.HTTP_200_OK)

    
@extend_schema(
        tags=["Password Reset"],
)
class PasswordResetTokenView(generics.GenericAPIView):
    serializer_class = PhoneRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, phone=serializer.data["phone"])
        auth_sms = user.authsms.last()

        if auth_sms.secure_code == serializer.data['secure_code']:
            time_difference = timezone.now() - auth_sms.created_at
            if time_difference.total_seconds() > 120:
                return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({"error": AuthSms.WRONG_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)
        

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        return Response({"token": f"{encoded_pk}/{token}"}, status=status.HTTP_200_OK)


@extend_schema(
        tags=["Password Reset"],
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password reset complete"),
        }
)
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        return Response({"detail": User.PASSWORD_REST}, status=status.HTTP_200_OK)

