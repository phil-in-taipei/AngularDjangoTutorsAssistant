from rest_framework import serializers

from .models import RecurringScheduledClass, RecurringClassAppliedMonthly


class RecurringClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringScheduledClass
        day_of_week_string = serializers.ReadOnlyField()

        fields = (
            'id', 'student_or_class', 'teacher',
            'recurring_start_time', 'recurring_finish_time',
            'recurring_day_of_week', 'day_of_week_string'
        )


class RecurringClassAppliedMonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringClassAppliedMonthly
        month_string = serializers.ReadOnlyField()

        fields = (
            'id', 'scheduling_month', 'scheduling_year',
            'recurring_class', 'month_string'
        )
