from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'id', 'school_name', 'address_line_1',
            'address_line_2', 'contact_phone', 'other_information'
        )

