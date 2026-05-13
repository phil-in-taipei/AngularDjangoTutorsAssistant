from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import CheckConstraint, Q

from client_school.models import ClientSchool
from student_account.models import StudentOrClass

STUDENT_LEVEL = (
    ('beginner', 'Beginner'),
    ('pre-intermediate', 'Pre-intermediate'),
    ('intermediate', 'Intermediate'),
    ('upper-intermediate', 'Upper-intermediate'),
    ('advanced', 'Advanced'),
)

CLASS_ENROLLMENT_TYPES = (
    ('one_to_one_tutoring', 'One-to-one Tutoring'),
    ('two_to_one_tutoring', 'Two-to-one Tutoring'),
    ('online_tutoring', 'Online Tutoring'),
    ('group_class', 'Group Class'),
    ('company_class', 'Company Class'),
)

class StudentAccountBillingManager(models.Manager):
    def under_two_hours(self):
        return [
            account for account in self.get_queryset()
            if (
                (account.purchased_group_class_hours is not None and account.purchased_group_class_hours <= 2) or
                (account.purchased_tutoring_hours is not None and account.purchased_tutoring_hours <= 2) or
                (account.purchased_online_hours is not None and account.purchased_online_hours <= 2) or
                (account.purchased_company_hours is not None and account.purchased_company_hours <= 2)
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
    group_hours_expiration_date = models.DateField(
        blank=True, null=True
    )
    purchased_tutoring_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    tutoring_hours_expiration_date = models.DateField(
        blank=True, null=True
    )
    purchased_online_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    online_hours_expiration_date = models.DateField(
        blank=True, null=True
    )
    purchased_company_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    company_hours_expiration_date = models.DateField(
        blank=True, null=True
    )

    def __str__(self):
        return "{}, {}".format(
            self.client_student_name,
            self.client_school.school_name
        )
    
    class Meta:
        verbose_name_plural = 'Client School Student Accounts'
        unique_together = ('client_school', 'client_student_name')
        ordering = ('client_school__school_name', 'client_student_name')
        constraints = [
            CheckConstraint(
                check=(
                    (
                        Q(purchased_group_class_hours__isnull=True) &
                        Q(group_hours_expiration_date__isnull=True)
                    )
                    |
                    (
                        Q(purchased_group_class_hours__isnull=False) &
                        Q(group_hours_expiration_date__isnull=False)
                    )

                ),
                name='group_hours_expiration_date_null_check'
            ),
            CheckConstraint(
                check=(
                    (
                        Q(purchased_tutoring_hours__isnull=True) &
                        Q(tutoring_hours_expiration_date__isnull=True)
                    )
                    |
                    (
                        Q(purchased_tutoring_hours__isnull=False) &
                        Q(tutoring_hours_expiration_date__isnull=False)
                    )
                ),
                name='tutoring_hours_expiration_date_null_check'
            ),
            CheckConstraint(
                check=(
                    (
                        Q(purchased_online_hours__isnull=True) &
                        Q(online_hours_expiration_date__isnull=True)
                    )
                    |
                    (
                        Q(purchased_online_hours__isnull=False) &
                        Q(online_hours_expiration_date__isnull=False)
                    )
                ),
                name='online_hours_expiration_date_null_check'
            ),
            CheckConstraint(
                check=(
                    (
                        Q(purchased_company_hours__isnull=True) &
                        Q(company_hours_expiration_date__isnull=True)
                    )
                    |
                    (
                        Q(purchased_company_hours__isnull=False) &
                        Q(company_hours_expiration_date__isnull=False)
                    )
                ),
                name='company_hours_expiration_date_null_check'
            ),
        ]



class ClientSchoolClassEnrollmentHandler(models.Model):
    student_or_class = models.ForeignKey(
        StudentOrClass, on_delete=models.SET_NULL,
        related_name='teachers_student_or_class_record',
        blank=True, null=True
    )
    class_enrollment_type = models.CharField(
        max_length=200, choices=CLASS_ENROLLMENT_TYPES,
        default='one_to_one_tutoring'
    )
    client_school_one_to_one_account = models.ForeignKey(
        AccountingClientSchoolStudentAccount,
        on_delete=models.CASCADE,
        related_name='one_to_one_tutoring_enrollment',
        blank=True, null=True
    )
    client_school_two_to_one_accounts = models.ManyToManyField(
        AccountingClientSchoolStudentAccount,
        related_name='two_to_one_tutoring_enrollments',
        blank=True,
    )
    client_school_online_account = models.ForeignKey(
        AccountingClientSchoolStudentAccount,
        on_delete=models.CASCADE,
        related_name='online_enrollment',
        blank=True, null=True
    )
    client_school_company_account = models.ForeignKey(
        AccountingClientSchoolStudentAccount,
        on_delete=models.CASCADE,
        related_name='company_enrollment',
        blank=True, null=True
    )
    client_group_accounts = models.ManyToManyField(
        AccountingClientSchoolStudentAccount,
        related_name='group_class_enrollments',
        blank=True,
    )

    def __str__(self):
        return "{}, {}".format(
            self.student_or_class,
            self.class_enrollment_type
        )

    def clean(self):
        if self.class_enrollment_type == 'one_to_one_tutoring':
            if self.client_school_one_to_one_account is None:
                raise ValidationError(
                    'One-to-one tutoring requires a client_school_one_to_one_account.'
                )
            if self.client_school_online_account is not None:
                raise ValidationError(
                    'One-to-one tutoring cannot have an online account.'
                )
            if self.client_school_company_account is not None:
                raise ValidationError(
                    'One-to-one tutoring cannot have a company account.'
                )

        elif self.class_enrollment_type == 'two_to_one_tutoring':
            if self.client_school_one_to_one_account is not None:
                raise ValidationError(
                    'Two-to-one tutoring cannot have a one-to-one account.'
                )
            if self.client_school_online_account is not None:
                raise ValidationError(
                    'Two-to-one tutoring cannot have an online account.'
                )
            if self.client_school_company_account is not None:
                raise ValidationError(
                    'Two-to-one tutoring cannot have a company account.'
                )

        elif self.class_enrollment_type == 'online_tutoring':
            if self.client_school_online_account is None:
                raise ValidationError(
                    'Online tutoring requires a client_school_online_account.'
                )
            if self.client_school_one_to_one_account is not None:
                raise ValidationError(
                    'Online tutoring cannot have a one-to-one account.'
                )
            if self.client_school_company_account is not None:
                raise ValidationError(
                    'Online tutoring cannot have a company account.'
                )

        elif self.class_enrollment_type == 'group_class':
            if self.client_school_one_to_one_account is not None:
                raise ValidationError(
                    'Group class cannot have a one-to-one account.'
                )
            if self.client_school_online_account is not None:
                raise ValidationError(
                    'Group class cannot have an online account.'
                )
            if self.client_school_company_account is not None:
                raise ValidationError(
                    'Group class cannot have a company account.'
                )

        elif self.class_enrollment_type == 'company_class':
            if self.client_school_company_account is None:
                raise ValidationError(
                    'Company class requires a client_school_company_account.'
                )
            if self.client_school_one_to_one_account is not None:
                raise ValidationError(
                    'Company class cannot have a one-to-one account.'
                )
            if self.client_school_online_account is not None:
                raise ValidationError(
                    'Company class cannot have an online account.'
                )

        if self.pk:
            if self.class_enrollment_type == 'two_to_one_tutoring':
                count = self.client_school_two_to_one_accounts.count()
                if count > 2:
                    raise ValidationError(
                        'Two-to-one tutoring cannot have more than 2 student accounts.'
                    )
                if self.client_group_accounts.exists():
                    raise ValidationError(
                        'Two-to-one tutoring cannot have group class accounts.'
                    )

            elif self.class_enrollment_type == 'group_class':
                if self.client_school_two_to_one_accounts.exists():
                    raise ValidationError(
                        'Group class cannot have two-to-one tutoring accounts.'
                    )

            elif self.class_enrollment_type in (
                'one_to_one_tutoring', 'online_tutoring', 'company_class'
            ):
                if self.client_school_two_to_one_accounts.exists():
                    raise ValidationError(
                        '{} cannot have two-to-one tutoring accounts.'.format(
                            self.get_class_enrollment_type_display()
                        )
                    )
                if self.client_group_accounts.exists():
                    raise ValidationError(
                        '{} cannot have group class accounts.'.format(
                            self.get_class_enrollment_type_display()
                        )
                    )

    class Meta:
        verbose_name_plural = 'Client School Class Enrollment Handlers'
        ordering = ('student_or_class__teacher__surname', 'class_enrollment_type')
        constraints = [
            CheckConstraint(
                check=(
                    (
                        Q(class_enrollment_type='one_to_one_tutoring')
                        & Q(client_school_one_to_one_account__isnull=False)
                        & Q(client_school_online_account__isnull=True)
                        & Q(client_school_company_account__isnull=True)
                    )
                    |
                    (
                        Q(class_enrollment_type='two_to_one_tutoring')
                        & Q(client_school_one_to_one_account__isnull=True)
                        & Q(client_school_online_account__isnull=True)
                        & Q(client_school_company_account__isnull=True)
                    )
                    |
                    (
                        Q(class_enrollment_type='online_tutoring')
                        & Q(client_school_online_account__isnull=False)
                        & Q(client_school_one_to_one_account__isnull=True)
                        & Q(client_school_company_account__isnull=True)
                    )
                    |
                    (
                        Q(class_enrollment_type='group_class')
                        & Q(client_school_one_to_one_account__isnull=True)
                        & Q(client_school_online_account__isnull=True)
                        & Q(client_school_company_account__isnull=True)
                    )
                    |
                    (
                        Q(class_enrollment_type='company_class')
                        & Q(client_school_company_account__isnull=False)
                        & Q(client_school_one_to_one_account__isnull=True)
                        & Q(client_school_online_account__isnull=True)
                    )
                ),
                name='enrollment_type_fk_consistency_check'
            )
        ]
