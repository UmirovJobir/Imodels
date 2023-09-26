from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import phone_regex
from .managers import UserManager


class User(AbstractUser):
    _USER_ERROR_MESSAGE = "Bunday foydalanuvchi topilmadi"
    
    username = None
    phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=17, unique=True)
    eskiz_id = models.CharField(max_length=20, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=False)
    eskiz_code = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = UserManager()


class AuthSms(models.Model):
    _WRONG_SECURE_CODE = "Wrong security code"
    _SECURE_CODE_EXPIRED = "Security code has expired"
    _USER_ACTIVETED = "User activated"
    _SECURE_CODE_RESENT = "The security code has been resent"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    secure_code = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)