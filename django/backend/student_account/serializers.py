from rest_framework import serializers

from .models import StudentOrClass


class StudentOrClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOrClass
        fields = (
            'id', 'student_or_class_name', 'account_type', 'school',
            'comments', 'purchased_class_hours', 'tuition_per_hour',
            'account_id', 'slug'
        )
