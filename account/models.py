from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import phone_regex
from .managers import UserManager


class User(AbstractUser):
    INVALID_PASSWORD = "Invalid password. Password must be at least 8 characters long."
    USER_ERROR_MESSAGE = "User not found"
    PASSWORD_REST = "Password reset complete"
    
    AUTH_VERIFY_CODE_TEXT = "iModels web sahifasi uchun tasdiqlash kodi: {}"
    INVALID_SECURE_CODE = "Invalid security code"
    SECURE_CODE_EXPIRED = "Security code has expired"
    USER_ACTIVETED = "User activated"
    SECURE_CODE_RESENT = "The security code has been sent"
    
    username = None
    phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=17, unique=True)
    secure_code = models.CharField(max_length=6, blank=True, null=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    new_phone_temp = models.CharField(max_length=17, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


# class AuthSms(models.Model):
#     AUTH_VERIFY_CODE_TEXT = "iModels web sahifasi uchun tasdiqlash kodi: {}"
#     INVALID_SECURE_CODE = "Invalid security code"
#     SECURE_CODE_EXPIRED = "Security code has expired"
#     USER_ACTIVETED = "User activated"
#     SECURE_CODE_RESENT = "The security code has been sent"
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authsms')
#     secure_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Auth Sms"
#         verbose_name_plural = 'Auth Sms'


# class NewPhone(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new_phone')
#     phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=17, unique=True)
#     secure_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)