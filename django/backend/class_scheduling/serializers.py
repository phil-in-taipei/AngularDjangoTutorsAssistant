from rest_framework import serializers
from .models import ScheduledClass


class ScheduledClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledClass
        student_or_class_template_str = serializers.ReadOnlyField()
        fields = (
            'id', 'student_or_class',
            'date', 'teacher',
            'start_time', 'finish_time',
            'class_status', 'teacher_notes',
            'class_content', 'student_or_class_template_str'
        )
