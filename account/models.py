from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


# class CustomUser(AbstractUser):
#     username = None
#     phone_number = models.CharField(max_length=12, unique=True, validators=[validate_phone_length])

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.phone_number
    

class User(AbstractUser):
    _USER_ERROR_MESSAGE = "Bunday foydalanuvchi topilmadi"
    
    """User model."""
    username = None
    phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message="Faqat o'zbek raqamlarigina tasdiqlanadi")
    phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=17, unique=True)
    eskiz_id = models.CharField(max_length=20, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=False)
    eskiz_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    @property
    def isVerified(self):
        return self.is_verified
