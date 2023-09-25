from django.core.exceptions import ValidationError


def validate_phone_length(value):
    if len(value) != 12:
        raise ValidationError('Phone number must be exactly 12 digits.')
