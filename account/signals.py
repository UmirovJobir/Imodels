from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from libs.sms import client
from libs.telegram import send_message

from .models import AuthSms

@receiver(post_save, sender=AuthSms)
def send_order_confirmation_message(sender, instance, created, **kwargs):
    if created:
        send_message(
                type='auth',
                text=AuthSms.AUTH_VERIFY_CODE_TEXT.format(instance.secure_code))
        
        if settings.DEBUG==False:
            client._send_sms(
                phone_number=instance.user.phone,
                message=AuthSms.AUTH_VERIFY_CODE_TEXT.format(instance.secure_code))
