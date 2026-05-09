from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from user_profiles.models import UserProfile


class ClientSchool(models.Model):
    school_name = models.CharField(max_length=200)
    school_owner = models.ForeignKey(
        UserProfile, limit_choices_to={'account_type': 'client_school_owner'},
        null=True, blank=True, on_delete=models.CASCADE
    )
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120)
    contact_email = models.EmailField(max_length=200, null=True, blank=True)
    contact_phone = models.CharField(
        max_length=10, null=True, blank=True, validators=[
            RegexValidator(
                regex='^\d{10}$',
                message='Length has to be 10',
                code='Invalid number'
            )
        ]
    )
    other_information = models.TextField(editable=True, default='', blank=True)

    def __str__(self):
        return self.school_name

    class Meta:
        ordering = ['school_name']