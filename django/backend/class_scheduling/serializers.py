from rest_framework import serializers

from user_profiles.serializers import UserProfileSerializer
from student_account.serializers import StudentOrClassGoogleCalendarSerializer
from .models import ScheduledClass


class ScheduledClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledClass
        fields = (
            'id', 'student_or_class',
            'date', 'teacher',
            'start_time', 'finish_time',
            'class_status', 'teacher_notes',
            'class_content'
        )

class ScheduledClassGoogleCalendarSerializer(serializers.ModelSerializer):
    teacher = UserProfileSerializer(read_only=True)
    student_or_class = StudentOrClassGoogleCalendarSerializer(
        read_only=True
    )

    class Meta:
        model = ScheduledClass
        fields = (
            'id', 'student_or_class',
            'date', 'teacher',
            'start_time', 'finish_time',
            'class_status'
        )

