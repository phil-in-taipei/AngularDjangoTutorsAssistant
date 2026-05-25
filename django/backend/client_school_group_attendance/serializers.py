from rest_framework import serializers
from client_school_group_attendance.models import (
    GroupClassMeetingRecord,
    GroupClassStudentAttendanceRecord,
)

CLASS_STATUS = (
    ('scheduled', 'Scheduled'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('same_day_cancellation', 'Same_Day_Cancellation'),
)

ATTENDANCE_CONFIRMATION_CHOICES = (
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('same_day_cancellation', 'Same_Day_Cancellation'),
)


class GroupClassStudentAttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student_account.client_student_name',
        read_only=True
    )

    class Meta:
        model = GroupClassStudentAttendanceRecord
        fields = (
            'id',
            'student_account',
            'student_name',
            'attendance_status',
            'time_stamp',
        )
        read_only_fields = ('student_account', 'student_name', 'time_stamp')


class GroupClassMeetingRecordSerializer(serializers.ModelSerializer):
    student_attendance_records = GroupClassStudentAttendanceRecordSerializer(
        many=True, read_only=True
    )
    group_class_name = serializers.CharField(
        source='group_class.group_class_name',
        read_only=True
    )

    class Meta:
        model = GroupClassMeetingRecord
        fields = (
            'id',
            'scheduled_class',
            'group_class',
            'group_class_name',
            'teacher_name',
            'class_date',
            'class_duration',
            'time_stamp',
            'student_attendance_records',
        )
        read_only_fields = (
            'scheduled_class',
            'group_class',
            'group_class_name',
            'teacher_name',
            'class_date',
            'class_duration',
            'time_stamp',
        )


class GroupClassStudentAttendanceRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupClassStudentAttendanceRecord
        fields = ('id', 'attendance_status')

    def validate_attendance_status(self, value):
        valid_choices = [choice[0] for choice in ATTENDANCE_CONFIRMATION_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Attendance status must be one of: {', '.join(valid_choices)}"
            )
        return value
