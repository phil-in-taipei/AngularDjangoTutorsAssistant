from django.db import models
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile


CLASS_STATUS = (
    ('scheduled', 'Scheduled'),
    #('cancellation_request', 'Cancellation_Request'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('same_day_cancellation', 'Same_Day_Cancellation'),
)


class ScheduledClassManager(models.Manager):

    def already_booked_classes_during_date_and_time(
            self, query_date, starting_time, finishing_time,
    ):
        class_booked_on_date = self.get_queryset().filter(
            date=query_date,
        )

        class_starts_during_time_frame = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time <= scheduled_class.start_time <= finishing_time
        ]

        class_finishes_during_time_frame = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time <= scheduled_class.finish_time <= finishing_time
        ]

        time_frame_occurs_during_a_booked_class = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time >= scheduled_class.start_time
            and finishing_time <= scheduled_class.finish_time
        ]

        classes_during_date_and_time = [
            scheduled_class for scheduled_class in class_booked_on_date
            if scheduled_class in class_starts_during_time_frame or
            scheduled_class in class_finishes_during_time_frame or
            scheduled_class in time_frame_occurs_during_a_booked_class
        ]

        return classes_during_date_and_time

    def student_or_class_already_booked_classes_during_date_and_time(
            self, query_date, starting_time, finishing_time, student_or_class_id
    ):
        class_booked_on_date = self.get_queryset().filter(
            date=query_date,
            student_or_class_id=student_or_class_id
        )

        class_starts_during_time_frame = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time <= scheduled_class.start_time <= finishing_time
        ]

        class_finishes_during_time_frame = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time <= scheduled_class.finish_time <= finishing_time
        ]

        time_frame_occurs_during_a_booked_class = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time >= scheduled_class.start_time
            and finishing_time <= scheduled_class.finish_time
        ]

        classes_during_date_and_time = [
            scheduled_class for scheduled_class in class_booked_on_date
            if scheduled_class in class_starts_during_time_frame or
            scheduled_class in class_finishes_during_time_frame or
            scheduled_class in time_frame_occurs_during_a_booked_class
        ]

        return len(classes_during_date_and_time) > 0

    def teacher_already_booked_classes_during_date_and_time(
            self, query_date, starting_time, finishing_time, teacher_id
    ):
        class_booked_on_date = self.get_queryset().filter(
            date=query_date,
            teacher_id=teacher_id
        )

        class_starts_during_time_frame = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time <= scheduled_class.start_time <= finishing_time
        ]

        class_finishes_during_time_frame = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time <= scheduled_class.finish_time <= finishing_time
        ]

        time_frame_occurs_during_a_booked_class = [
            scheduled_class for scheduled_class in class_booked_on_date
            if starting_time >= scheduled_class.start_time
            and finishing_time <= scheduled_class.finish_time
        ]

        classes_during_date_and_time = [
            scheduled_class for scheduled_class in class_booked_on_date
            if scheduled_class in class_starts_during_time_frame or
            scheduled_class in class_finishes_during_time_frame or
            scheduled_class in time_frame_occurs_during_a_booked_class
        ]

        return len(classes_during_date_and_time) > 0

    def teacher_already_booked_classes_on_date(
            self, query_date, teacher_id
    ):
        return self.get_queryset().filter(
            date=query_date,
            teacher_id=teacher_id
        )


class ScheduledClass(models.Model):
    custom_query = ScheduledClassManager()
    objects = models.Manager()
    student_or_class = models.ForeignKey(
        StudentOrClass, related_name='scheduled_student_or_class',
        on_delete=models.CASCADE)

    teacher = models.ForeignKey(
        UserProfile, related_name='scheduled_teacher', on_delete=models.CASCADE
    )
    date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField()
    class_status = models.CharField(max_length=300,
                                    choices=CLASS_STATUS,
                                    default='scheduled')
    teacher_notes = models.TextField(editable=True, default='',
                                     blank=True)
    class_content = models.TextField(editable=True, default='',
                                     blank=True)

    def __str__(self):
        return "{} on {} at {}-{} with {}".format(
            str(self.teacher).title(), self.date,
            str(self.start_time)[:-3], str(self.finish_time)[:-3],
            str(self.student_or_class).title()
        )

    class Meta:
        verbose_name_plural = 'Scheduled Classes'
        ordering = ['-date', 'teacher', 'start_time']
