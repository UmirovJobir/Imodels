from django.core.validators import RegexValidator


phone_regex = RegexValidator(
                regex=r'^998[0-9]{2}[0-9]{7}$',
                message="Faqat o'zbek raqamlarigina tasdiqlanadi"
            )

def is_valid_password(password):
    return len(password) >= 8