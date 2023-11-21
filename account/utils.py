from random import choice
from django.conf import settings


def generate_code() -> str:
    """Generates random verify code"""
    password: str = ''
    numbers: tuple = ('1234567890')
    
    if settings.DEBUG==False:
        for _ in range(6):
            password+=choice(choice(numbers))
    else:
        password = '111111'
    
    return password
