from rest_framework import serializers

from class_scheduling.serializers import ScheduledClassSerializer
from .models import FreelanceTuitionTransactionRecord, PurchasedHoursModificationRecord


class FreelanceTuitionTransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelanceTuitionTransactionRecord
        fields = "__all__"


class PurchasedHoursModificationRecordSerializer(serializers.ModelSerializer):
    tuition_transaction = FreelanceTuitionTransactionRecordSerializer(read_only=True)
    modified_scheduled_class = ScheduledClassSerializer(read_only=True)

    class Meta:
        model = PurchasedHoursModificationRecord
        fields = "__all__"
