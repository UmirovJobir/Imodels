from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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

from libs.telegram import send_message
from libs.sms import client

from .utils import generate_code
from .models import User
from .serializers import (
    RegisterSerializer,
    ConfirmSerializer,
    ResendSecureCodeSerializer,
    UserSerializer,
    ConfirmPhoneSerializer,
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
class RegisterConfirmView(generics.CreateAPIView):
    serializer_class = ConfirmSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "detail": User.USER_ACTIVETED,
        }, status=status.HTTP_200_OK)


@extend_schema(
        tags=["User"],
        request = UserSerializer,
         responses={
            200: OpenApiResponse(description=f"(Phone number updated successfully, {User.SECURE_CODE_RESENT})"),
        }
        
)
class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        if serializer.context.get('secure_code_sent'):
            return Response({"detail": User.SECURE_CODE_RESENT}, status=status.HTTP_200_OK)

        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(
        tags=["User"],
        request=ConfirmPhoneSerializer,
        responses={
            200: OpenApiResponse(description=f"Phone number updated successfully"),
            400: OpenApiResponse(description=f"{User.INVALID_SECURE_CODE, User.SECURE_CODE_EXPIRED}"),
        },
)
class ConfirmUpdateView(generics.GenericAPIView):
    serializer_class = ConfirmPhoneSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Phone number updated successfully.",
        }, status=status.HTTP_200_OK)



@extend_schema(
        tags=["Password Reset"],
        request=PhoneResetSerializer,
        responses={
            200: OpenApiResponse(description="Created. New resource in response"),
            404: OpenApiResponse(description="Not found"),
        },
)
class ResendSecureCodeView(generics.GenericAPIView):
    serializer_class = ResendSecureCodeSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "detail": User.SECURE_CODE_RESENT
        }, status=status.HTTP_200_OK)

    
@extend_schema(
        tags=["Password Reset"],
)
class PasswordResetTokenView(generics.GenericAPIView):
    serializer_class = ConfirmSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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

