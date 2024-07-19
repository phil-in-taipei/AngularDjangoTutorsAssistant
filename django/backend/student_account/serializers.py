from rest_framework import serializers

from .models import StudentOrClass


class StudentOrClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOrClass
        fields = '__all__'
