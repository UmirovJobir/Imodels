from rest_framework.response import Response
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.shortcuts import get_object_or_404

from libs.telegram import telebot
from .utils import generate_code
from .models import User, AuthSms
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class VerifyView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, phone=request.data.get('phone'))
        auth_sms = get_object_or_404(AuthSms, user=user)

        if auth_sms.secure_code != request.data.get('secure_code'):
            return Response({"error": AuthSms._WRONG_SECURE_CODE}, status=status.HTTP_400_BAD_REQUEST)

        time_difference = timezone.now() - auth_sms.created_at
        if time_difference.total_seconds() > 120:
            return Response({"error": AuthSms._SECURE_CODE_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_active=True
            user.save()
            return Response({"detail": AuthSms._USER_ACTIVETED}, status=status.HTTP_202_ACCEPTED)


class ResendView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, phone=request.data.get('phone'))

        auth_sms = AuthSms.objects.get(user=user)
        auth_sms.secure_code = generate_code()
        auth_sms.created_at = timezone.now()
        auth_sms.save()

        telebot.send_message(text=auth_sms.secure_code, _type='chat_id_orders')

        return Response({"detail": AuthSms._SECURE_CODE_RESENT}, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user