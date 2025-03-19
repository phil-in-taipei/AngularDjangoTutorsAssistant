from django.db import models
from decimal import Decimal
from django.db.models import CheckConstraint, Q
from class_scheduling.models import ScheduledClass
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from .utils import validate_number_of_hours_purchased


TRANSACTION_TYPE = (
        ('payment', 'Payment'),
        ('refund', 'Refund'),
)

ACCOUNT_BALANCE_ALTERATION_TYPE = (
    ('tuition_payment_add', 'Tuition Payment'),
    ('tuition_refund_deduct', 'Tuition Refund'),
    ('class_status_modification_add', "Class Status Modification: Hours Added"),
    ('class_status_modification_deduct', "Class Status Modification: Hours Deducted"),
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


class PurchasedHoursModificationRecord(models.Model):
    student_or_class = models.ForeignKey(
        StudentOrClass, on_delete=models.CASCADE,
        limit_choices_to={'account_type': 'freelance'},
        related_name='student_or_class_purchased_hours_modification',
    )
    tuition_transaction = models.OneToOneField(
        FreelanceTuitionTransactionRecord, on_delete=models.CASCADE,
        related_name='tuition_purchased_hours_modification',
        blank = True, null = True
    )
    modified_scheduled_class = models.ForeignKey(
        ScheduledClass, on_delete=models.CASCADE,
        related_name='class_status_purchased_hours_modification',
        blank = True, null = True
    )
    modification_type = models.CharField(
        max_length=200, choices=ACCOUNT_BALANCE_ALTERATION_TYPE,
        default='class_status_modification_deduct'
    )
    previous_purchased_class_hours = models.DecimalField(
        max_digits=5, decimal_places=2,
    )
    updated_purchased_class_hours = models.DecimalField(
        max_digits=5, decimal_places=2,
    )
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        formatted_time = self.time_stamp.strftime("%Y-%m-%d %H:%M")
        if self.tuition_transaction:
            formatted_amount = "${:,}".format(self.tuition_transaction.transaction_amount)
            return "Tuition Transaction ({}): {}hrs at {}".format(
                formatted_amount,
                str(self.tuition_transaction.class_hours_purchased_or_refunded),
                formatted_time
            )
        else:
            return "Class Status Modification: {} at {}".format(
                str(self.student_or_class.student_or_class_name).title(),
                formatted_time
            )

    class Meta:
        #unique_together = ('teacher', 'student_or_class_name')
        ordering = (
            'student_or_class__teacher',
            'time_stamp', 'student_or_class__student_or_class_name'
        )
        constraints = [
            CheckConstraint(
                check=(
                    (
                            Q(tuition_transaction__isnull=True)
                            & (
                                    Q(modification_type="class_status_modification_add")
                                    |
                                    Q(modification_type="class_status_modification_deduct")
                               )
                            & Q(modified_scheduled_class__isnull=False)
                    )
                    |
                    (
                        Q(odified_scheduled_class__isnull=True)
                        & (
                                Q(modification_type="tuition_payment_add")
                                |
                                Q(modification_type="tuition_refund_deduct")
                        )
                        & Q(tuition_transaction__isnull=False)
                    )

                ),
                name="tuition_transaction_modified_scheduled_class_null_check",
            )
        ]

