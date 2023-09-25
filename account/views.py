from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import RegisterSerializer, CustomUserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user