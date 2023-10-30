from django.db import models
from account.validators import phone_regex


class ContactRequest(models.Model):
    phone = models.CharField('Telefon raqam', validators=[phone_regex], max_length=17)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Murojat'
        verbose_name_plural = 'Murojatlar'