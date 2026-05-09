from django.db import models
from django.core.validators import MaxLengthValidator

from client_school.models import ClientSchool

STUDENT_LEVEL = (
    ('beginner', 'Beginner'),
    ('pre-intermediate', 'Pre-intermediate'),
    ('intermediate', 'Intermediate'),
    ('upper-intermediate', 'Upper-intermediate'),
    ('advanced', 'Advanced'),
)

class StudentAccountBillingManager(models.Manager):
    def under_two_hours(self):
        return [
            account for account in self.get_queryset()
            if (
                (account.purchased_group_class_hours is not None and account.purchased_group_class_hours <= 2) or
                (account.purchased_tutoring_hours is not None and account.purchased_tutoring_hours <= 2) or
                (account.purchased_online_hours is not None and account.purchased_online_hours <= 2)
            )
        ]


class AccountingClientSchoolStudentAccount(models.Model):
    custom_query = StudentAccountBillingManager()
    objects = models.Manager()
    client_student_name = models.CharField(max_length=200)
    client_school = models.ForeignKey(
        ClientSchool, on_delete=models.CASCADE,
        related_name='client_school',
    )
    contact_email = models.EmailField(max_length=200, null=True, blank=True)
    student_level = models.CharField(
        max_length=200, choices=STUDENT_LEVEL, default='intermediate'
    )
    comments = models.TextField(
        editable=True, validators=[MaxLengthValidator(500)],
        default='', blank=True
    )
    purchased_group_class_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    purchased_tutoring_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    purchased_online_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return "{}, {}".format(
            self.client_student_name,
            self.client_school.school_name
        )
    
    class Meta:
        verbose_name_plural = 'Client School Student Accounts'
        unique_together = ('client_school', 'client_student_name')
        ordering = ('client_student_name', 'client_student_name')