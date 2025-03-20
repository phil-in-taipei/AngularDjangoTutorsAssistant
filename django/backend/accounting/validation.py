from django.core.exceptions import ValidationError


def validate_number_of_hours_purchased(value):
    if value <= 100:
        return value
    else:
        raise ValidationError("100 is the maximum amount for purchase!")
   