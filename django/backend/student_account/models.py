from django.db import models
from django.core.validators import MaxLengthValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import CheckConstraint, Q

from school.models import School
from user_profiles.models import UserProfile
from utilities.general_utils import random_string_generator, validate_tuition_rate


ACCOUNT_TYPE = (
        ('freelance', 'Freelance'),
        ('school', 'School'),
    )


class StudentBillingManager(models.Manager):
    def under_two_hours(self):
        return [
            account for account in self.get_queryset()
            if account.purchased_class_hours <= 2
        ]


class StudentOrClass(models.Model):
    custom_query = StudentBillingManager()
    objects = models.Manager()
    student_or_class_name = models.CharField(max_length=200)
    account_type = models.CharField(
        max_length=200, choices=ACCOUNT_TYPE, default='freelance'
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        related_name='school', blank=True, null=True
    )
    teacher = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='teacher',
    )
    comments = models.TextField(
        editable=True, validators=[MaxLengthValidator(500)],
        default='', blank=True
    )
    purchased_class_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    tuition_per_hour = models.PositiveSmallIntegerField(
        validators=[validate_tuition_rate], default=900
    )
    account_id = models.CharField(max_length=10, null=True, blank=True)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('teacher', 'student_or_class_name')
        ordering = ('teacher__surname', 'student_or_class_name')
        constraints = [
            CheckConstraint(
                check=(
                    (
                        Q(purchased_class_hours__isnull=True)
                        & Q(account_type="school")
                        & Q(school__isnull=False)
                    )
                    |
                    (
                        Q(school__isnull=True)
                        & Q(account_type="freelance")
                        & Q(purchased_class_hours__isnull=False)
                    )
                ),
                name="school_freelance_null_check",
            )
        ]


@receiver(pre_save, sender=StudentOrClass)
def pre_save_account_id_and_slug(sender, **kwargs):
    # it will only create and save slug/account_id
    # fields for the post request because id == None
    if kwargs['instance'].id is None:
        random_string = random_string_generator()
        kwargs['instance'].account_id = random_string
        kwargs['instance'].slug = random_string
