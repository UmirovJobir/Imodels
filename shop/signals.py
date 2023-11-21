from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from libs.sms import client
from libs.telegram import send_message

from .models import ContactRequest

@receiver(post_save, sender=ContactRequest)
def send_order_confirmation_message(sender, instance, created, **kwargs):
    if created:
        send_message(type='contact', obj=instance)
        

