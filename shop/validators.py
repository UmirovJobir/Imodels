from django.core.exceptions import ValidationError


def validate_phone_length(value):
    if len(value) != 9:
        raise ValidationError('Phone number must be exactly 9 digits.')