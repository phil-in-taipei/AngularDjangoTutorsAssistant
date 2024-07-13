from django.db import models
from django.core.validators import RegexValidator


class School(models.Model):
    school_name = models.CharField(max_length=200, unique=True)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120)
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
