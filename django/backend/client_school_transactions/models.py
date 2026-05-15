from django.db import models
from decimal import Decimal
from django.core.validators import MaxLengthValidator
from client_school_accounting.models import (
    AccountingClientSchoolStudentAccount,
    ClientSchoolClassEnrollmentHandler,
)
from .validation import validate_tuition_transaction_amount
from accounting.validation import validate_number_of_hours_purchased


TRANSACTION_TYPE = (
    ('payment', 'Payment'),
    ('refund', 'Refund'),
)

GROUP_CLASS_EXPIRATION_PERIODS = (
    ('12_weeks', '12 Weeks'),
    ('30_weeks', '30 Weeks'),
    ('60_weeks', '60 Weeks'),
)

TUTORING_EXPIRATION_PERIODS = (
    ('6_months', '6 Months'),
    ('12_months', '12 Months'),
    ('24_months', '24 Months'),
)



class ClientSchoolTutoringTuitionTransactionRecord(models.Model):
    student_account = models.ForeignKey(
        AccountingClientSchoolStudentAccount, on_delete=models.CASCADE,
        related_name='tutoring_tuition_transactions',
        limit_choices_to={'purchased_tutoring_hours__isnull': False}
    )
    transaction_amount = models.PositiveSmallIntegerField(
        validators=[validate_tuition_transaction_amount], default=33000
    )
    transaction_type = models.CharField(
        max_length=200, choices=TRANSACTION_TYPE, default='payment'
    )
    class_hours_purchased_or_refunded = models.PositiveSmallIntegerField(
        validators=[validate_number_of_hours_purchased]
    )
    expiration_period = models.CharField(
        max_length=200, choices=TUTORING_EXPIRATION_PERIODS, default='6_months'
    )
    comments = models.TextField(
        editable=True, validators=[MaxLengthValidator(700)],
        default='', blank=True
    )
    administrator_name = models.CharField(
        max_length=200,
    )
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_time = self.time_stamp.strftime("%Y-%m-%d %H:%M")
        formatted_amount = "${:,}".format(self.transaction_amount)
        return "Tutoring {}: {} for {} at {}".format(
            self.transaction_type.capitalize(),
            self.student_account.client_student_name,
            formatted_amount,
            formatted_time
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        hours_as_decimal = Decimal(str(self.class_hours_purchased_or_refunded))
        if self.transaction_type == 'payment':
            self.student_account.purchased_tutoring_hours += hours_as_decimal
        else:
            self.student_account.purchased_tutoring_hours -= hours_as_decimal
        self.student_account.save()

    class Meta:
        verbose_name_plural = 'Tutoring Tuition Transaction Records'
        ordering = ('-time_stamp',)
