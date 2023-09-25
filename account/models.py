from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_phone_length
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=12, unique=True, validators=[validate_phone_length])

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
