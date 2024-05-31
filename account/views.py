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
from .models import User, AuthSms, NewPhone
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
            return Response({"error": AuthSms.INVALID_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - last_auth_sms.created_at
        if time_difference.total_seconds() > 120:
            return Response({"error": AuthSms.SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active=True
            user.save()
            return Response({"detail": AuthSms.USER_ACTIVETED}, status=status.HTTP_202_ACCEPTED)


@extend_schema(
        tags=["User"],
        responses={
            200: UserSerializer
        }
)
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
        tags=["User"],
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description=f"{AuthSms.INVALID_SECURE_CODE, AuthSms.SECURE_CODE_EXPIRED}"),
        },
)
class UserUpdateView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return self.update_user(request, partial=True)

    
    def update_user(self, request, partial):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
        tags=["User"],
        request=PhoneResetSerializer,
)
class UpdatePhoneView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        new_phone = request.data.get('phone')
        
        if not new_phone:
            return Response({"phone": "This field is required for phone number update."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        secure_code = generate_code()

        # Check if there is an existing NewPhone instance for this user and new phone number
        new_auth_sms, created = NewPhone.objects.update_or_create(
            user=user,
            phone=new_phone,
            defaults={
                'secure_code': secure_code,
                'created_at': timezone.now()
            }
        )

        return Response({"detail": AuthSms.SECURE_CODE_RESENT}, status=status.HTTP_200_OK)


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

