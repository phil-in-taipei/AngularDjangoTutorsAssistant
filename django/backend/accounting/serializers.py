from rest_framework import serializers

from class_scheduling.serializers import ScheduledClassSerializer
from student_account.serializers import StudentOrClassSerializer
from .models import FreelanceTuitionTransactionRecord, PurchasedHoursModificationRecord

class FreelanceTuitionTransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelanceTuitionTransactionRecord
        fields = "__all__"


class PurchasedHoursModificationRecordSerializer(serializers.ModelSerializer):
    student_or_class = StudentOrClassSerializer(read_only=True)
    tuition_transaction = FreelanceTuitionTransactionRecordSerializer(read_only=True)
    modified_scheduled_class = ScheduledClassSerializer(read_only=True)

    class Meta:
        model = PurchasedHoursModificationRecord
        fields = "__all__"
