from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    UserDetailView, 
    VerifyView, 
    ResendView, 
    PasswordResetTokenAPI,
    ResetPasswordAPI
)



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('resend/', ResendView.as_view(), name='resend'),

    path("password-reset/", PasswordResetTokenAPI.as_view(), name="password-reset-token"),
    path("password-reset/<str:encoded_pk>/<str:token>/", ResetPasswordAPI.as_view(), name="password-reset"),

    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]