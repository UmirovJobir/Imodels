from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    UserDetailView, 
    ConfirmView, 
    ResendView, 
    PasswordResetTokenView,
    ResetPasswordView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView
)



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('resend/', ResendView.as_view(), name='resend'),

    path("password-reset/", ResendView.as_view(), name="password-reset"),
    path("password-reset/confirm/", PasswordResetTokenView.as_view(), name="password-reset-confirm"),
    path("password-reset/<str:encoded_pk>/<str:token>/", ResetPasswordView.as_view(), name="password-reset"),

    path('user-detail/', UserDetailView.as_view(), name='user-detail'),

    # path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]