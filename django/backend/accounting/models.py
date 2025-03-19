from django.db import models
from decimal import Decimal
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from .utils import validate_number_of_hours_purchased


TRANSACTION_TYPE = (
        ('payment', 'Payment'),
        ('refund', 'Refund'),
)


class FreelanceTuitionTransactionRecord(models.Model):
    student_or_class = models.ForeignKey(
        StudentOrClass, on_delete=models.CASCADE,
        limit_choices_to={'account_type': 'freelance'},
        related_name='student_or_class_tuition_transactions',
    )
    transaction_amount = models.PositiveSmallIntegerField(editable=False)
    transaction_type = models.CharField(
        max_length=200, choices=TRANSACTION_TYPE, default='payment'
    )
    class_hours_purchased_or_refunded = models.PositiveSmallIntegerField(
        validators=[validate_number_of_hours_purchased])
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        formatted_time = self.time_stamp.strftime("%Y-%m-%d %H:%M")
        formatted_amount = "${:,}".format(self.transaction_amount)
        return "{}: {} for {} at {}".format(
            self.transaction_type.capitalize(),
            self.student_or_class.student_or_class_name,
            formatted_amount, formatted_time
        )

    def save(self, *args, **kwargs):
        self.transaction_amount = self.student_or_class.tuition_per_hour * \
                                self.class_hours_purchased_or_refunded
        super(FreelanceTuitionTransactionRecord, self).save(*args, **kwargs)
        # updates the account balance in the foreign key field
        hours_as_decimal = Decimal(str(self.class_hours_purchased_or_refunded))
        if self.transaction_type == "payment":
            print("......making the transaction now......")
            print(self.student_or_class.purchased_class_hours)
            self.student_or_class.purchased_class_hours += hours_as_decimal
        else:
            self.student_or_class.purchased_class_hours -= hours_as_decimal
        self.student_or_class.save()
