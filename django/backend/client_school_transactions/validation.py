from django.core.exceptions import ValidationError


def validate_tuition_transaction_amount(value):
    if 10000 <= value <= 200000:
        return value
    else:
        raise ValidationError("Tuition purchases between NT$10,000 and NT$200,000 only")
   