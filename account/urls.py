from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    UserDetailView,
    ConfirmUpdateView,
    RegisterConfirmView, 
    ResendSecureCodeView,
    PasswordResetTokenView,
    ResetPasswordView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/confirm/', RegisterConfirmView.as_view(), name='register-confirm'),
    path('resend/', ResendSecureCodeView.as_view(), name='resend'),

    path("password-reset/", ResendSecureCodeView.as_view(), name="password-reset"),
    path("password-reset/confirm/", PasswordResetTokenView.as_view(), name="password-reset-confirm"),
    path("password-reset/<str:encoded_pk>/<str:token>/", ResetPasswordView.as_view(), name="password-reset"),

    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('user-detail/confirm/', ConfirmUpdateView.as_view(), name='update-confirm'),
    
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]