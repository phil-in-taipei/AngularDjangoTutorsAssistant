from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from user_profiles.models import UserProfile


class Venue(models.Model):
    venue_name = models.CharField(max_length=200)
    venue_owner = models.ForeignKey(
        UserProfile, limit_choices_to={'account_type': 'venue_owner'},
        null=True, blank=True, on_delete=models.CASCADE
    )
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
        return self.venue_name

    class Meta:
        ordering = ['venue_name']


class VenueSpace(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    space_name = models.CharField(max_length=100)
    number_of_seats = models.PositiveSmallIntegerField(
        default=2, validators=[MinValueValidator(1), MaxValueValidator(15)]
    )

    def __str__(self):
        return "{} {}: {} seats".format(self.venue, self.space_name, self.number_of_seats)

    class Meta:
        unique_together = ['venue', 'space_name']
        ordering = ['venue__venue_name', 'space_name']
