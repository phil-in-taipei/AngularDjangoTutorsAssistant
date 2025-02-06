from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from student_account.models import StudentOrClass
from user_profiles.models import UserProfile

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

DAYS_OF_WEEK_INTEGERS = (
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday'),
    )


JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 11
DECEMBER = 12

MONTH_INTEGERS = (
    (JANUARY, 'January'),
    (FEBRUARY, 'February'),
    (MARCH, 'March'),
    (APRIL, 'April'),
    (MAY, 'May'),
    (JUNE, 'June'),
    (JULY, 'July'),
    (AUGUST, 'August'),
    (SEPTEMBER, 'September'),
    (OCTOBER, 'October'),
    (NOVEMBER, 'November'),
    (DECEMBER, 'December'),
    )


class RecurringScheduledClass(models.Model):
    recurring_start_time = models.TimeField(blank=True, null=True)
    recurring_finish_time = models.TimeField(blank=True, null=True)
    recurring_day_of_week = models.SmallIntegerField(choices=DAYS_OF_WEEK_INTEGERS)
    student_or_class = models.ForeignKey(
        StudentOrClass, related_name='recurring_student_or_class',
        on_delete=models.CASCADE)

    teacher = models.ForeignKey(
        UserProfile, related_name='recurring_teacher', on_delete=models.CASCADE
    )

    @property
    def day_of_week_string(self):
        day_of_week_string = [day[1] for day in DAYS_OF_WEEK_INTEGERS
                              if day[0] == self.recurring_day_of_week][0]
        return day_of_week_string

    def __str__(self):
        day_of_week_string = [day[1] for day in DAYS_OF_WEEK_INTEGERS
                              if day[0] == self.recurring_day_of_week][0]
        return "{} on {} from {} to {}".format(self.student_or_class,
                                               day_of_week_string,
                                               self.recurring_start_time,
                                               self.recurring_finish_time
                                               )
