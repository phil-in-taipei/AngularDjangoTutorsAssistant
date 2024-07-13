import random
import string
from django.core.exceptions import ValidationError


def random_string_generator(
        size=10, chars=string.ascii_lowercase + string.digits
):
    return ''.join(random.choice(chars) for _ in range(size))


def validate_tuition_rate(value):
    if 500 < value <= 2000:
        return value
    else:
        raise ValidationError("That rate is invalid!")


def validate_number_of_hours_purchased(value):
    if value <= 100:
        return value
    else:
        raise ValidationError("100 is the maximum amount for purchase!")
