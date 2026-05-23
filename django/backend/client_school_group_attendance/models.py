from django.db import models
from django.core.validators import MaxLengthValidator
from class_scheduling.models import ScheduledClass
from client_school_accounting.models import (
    AccountingClientSchoolGroupClass,
    AccountingClientSchoolStudentAccount,
)

CLASS_STATUS = (
    ('scheduled', 'Scheduled'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('same_day_cancellation', 'Same_Day_Cancellation'),
)


class GroupClassMeetingRecord(models.Model):
    scheduled_class = models.OneToOneField(
        ScheduledClass, on_delete=models.SET_NULL,
        related_name='group_class_meeting_record',
        blank=True, null=True
    )
    group_class = models.ForeignKey(
        AccountingClientSchoolGroupClass, on_delete=models.CASCADE,
        related_name='group_class_meeting_records',
    )
    teacher_name = models.CharField(max_length=200)
    class_date = models.DateField()
    class_duration = models.DecimalField(max_digits=4, decimal_places=2)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} — {} on {}".format(
            self.group_class.group_class_name,
            self.teacher_name,
            self.class_date,
        )

    class Meta:
        verbose_name_plural = 'Group Class Meeting Records'
        ordering = ('-class_date', 'group_class__group_class_name')


class GroupClassStudentAttendanceRecord(models.Model):
    group_class_meeting_record = models.ForeignKey(
        GroupClassMeetingRecord, on_delete=models.CASCADE,
        related_name='student_attendance_records',
    )
    student_account = models.ForeignKey(
        AccountingClientSchoolStudentAccount, on_delete=models.CASCADE,
        related_name='group_class_attendance_records',
    )
    attendance_status = models.CharField(
        max_length=300, choices=CLASS_STATUS, default='scheduled'
    )
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} — {} — {}".format(
            self.group_class_meeting_record,
            self.student_account.client_student_name,
            self.attendance_status,
        )

    class Meta:
        verbose_name_plural = 'Group Class Student Attendance Records'
        ordering = (
            '-group_class_meeting_record__class_date',
            'student_account__client_student_name',
        )
        unique_together = (
            'group_class_meeting_record', 'student_account'
        )
