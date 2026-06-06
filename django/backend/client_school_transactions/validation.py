from django.core.exceptions import ValidationError


def validate_tuition_transaction_amount(value):
    if 0 <= value <= 175000:
        return value
    else:
        raise ValidationError("Tuition transactions for less than NT$175,000 only")
   