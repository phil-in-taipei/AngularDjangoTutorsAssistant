from staff_admin.sites import staff_admin_site
from django.contrib import admin
from django.contrib import messages
from rangefilter.filters import DateRangeFilter

from client_school_group_attendance.models import (
    GroupClassMeetingRecord,
    GroupClassStudentAttendanceRecord,
)
from client_school_group_attendance.utils import (
    handle_group_class_attendance_hours_modification,
)


class StaffGroupClassMeetingRecordAdmin(admin.ModelAdmin):
    readonly_fields = (
        'scheduled_class',
        'group_class',
        'teacher_name',
        'class_date',
        'class_duration',
        'time_stamp',
    )
    list_display = (
        'group_class',
        'teacher_name',
        'class_date',
        'class_duration',
        'time_stamp',
    )
    ordering = ('-class_date',)
    search_fields = [
        'group_class__group_class_name',
        'teacher_name',
    ]
    list_filter = (
        ('class_date', DateRangeFilter),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StaffGroupClassStudentAttendanceRecordAdmin(admin.ModelAdmin):
    readonly_fields = (
        'group_class_meeting_record',
        'student_account',
        'time_stamp',
    )
    list_display = (
        'group_class_meeting_record',
        'student_account',
        'attendance_status',
        'time_stamp',
    )
    ordering = (
        '-group_class_meeting_record__class_date',
        'student_account__client_student_name',
    )
    search_fields = [
        'student_account__client_student_name',
        'group_class_meeting_record__group_class__group_class_name',
        'group_class_meeting_record__teacher_name',
    ]
    list_filter = (
        ('group_class_meeting_record__class_date', DateRangeFilter),
        'attendance_status',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if change:
            previous_status = GroupClassStudentAttendanceRecord.objects.get(
                pk=obj.pk
            ).attendance_status
            super().save_model(request, obj, form, change)
            modification_message = handle_group_class_attendance_hours_modification(
                attendance_record=obj,
                previous_status=previous_status,
            )
            if modification_message:
                self.message_user(
                    request,
                    modification_message,
                    level=messages.SUCCESS
                )
        else:
            super().save_model(request, obj, form, change)


staff_admin_site.register(GroupClassMeetingRecord, StaffGroupClassMeetingRecordAdmin)
staff_admin_site.register(
    GroupClassStudentAttendanceRecord,
    StaffGroupClassStudentAttendanceRecordAdmin
)
