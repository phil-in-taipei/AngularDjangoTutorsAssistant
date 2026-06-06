from django.core.exceptions import ValidationError


def validate_number_of_hours_purchased(value):
    if value <= 120:
        return value
    else:
        raise ValidationError("120 is the maximum amount for purchase!")
   