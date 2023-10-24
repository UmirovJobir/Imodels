from django.conf import settings
from eskiz.client import SMSClient


client = SMSClient(**settings.MYSERVICE.get('sms_service'))
