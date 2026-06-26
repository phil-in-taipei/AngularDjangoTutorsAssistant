from rest_framework import serializers
from client_school_accounting.models import (
    AccountingClientSchoolStudentAccount,
)
from .models import CSPurchasedHoursModification


class CSTransactionSummarySerializer(serializers.Serializer):
    transaction_amount = serializers.SerializerMethodField()
    transaction_type = serializers.SerializerMethodField()
    class_hours_purchased_or_refunded = serializers.SerializerMethodField()
    administrator_name = serializers.SerializerMethodField()
    transaction_time_stamp = serializers.SerializerMethodField()
    # Only non-null for two_to_one transactions
    shared_student_name = serializers.SerializerMethodField()

    def _get_transaction(self, obj):
        for attr in (
            'tutoring_transaction',
            'two_to_one_transaction',
            'online_transaction',
            'group_transaction',
            'company_transaction',
        ):
            tx = getattr(obj, attr, None)
            if tx is not None:
                return tx
        return None

    def get_transaction_amount(self, obj):
        tx = self._get_transaction(obj)
        return tx.transaction_amount if tx else None

    def get_transaction_type(self, obj):
        tx = self._get_transaction(obj)
        return tx.transaction_type if tx else None

    def get_class_hours_purchased_or_refunded(self, obj):
        tx = self._get_transaction(obj)
        return tx.class_hours_purchased_or_refunded if tx else None

    def get_administrator_name(self, obj):
        tx = self._get_transaction(obj)
        return tx.administrator_name if tx else None

    def get_transaction_time_stamp(self, obj):
        tx = self._get_transaction(obj)
        return tx.time_stamp if tx else None

    def get_shared_student_name(self, obj):
        tx = obj.two_to_one_transaction
        if tx is not None:
            return tx.shared_student_account.client_student_name
        return None


class CSPurchasedHoursModificationSerializer(serializers.ModelSerializer):
    class_type_display = serializers.CharField(
        source='get_class_type_display', read_only=True
    )
    modification_type_display = serializers.CharField(
        source='get_modification_type_display', read_only=True
    )
    hours_delta = serializers.SerializerMethodField()
    transaction_summary = serializers.SerializerMethodField()

    class Meta:
        model = CSPurchasedHoursModification
        fields = (
            'id',
            'class_type',
            'class_type_display',
            'modification_type',
            'modification_type_display',
            'previous_hours',
            'updated_hours',
            'hours_delta',
            'transaction_summary',
            'time_stamp',
        )

    def get_hours_delta(self, obj):
        return float(obj.updated_hours - obj.previous_hours)

    def get_transaction_summary(self, obj):
        has_transaction = any([
            obj.tutoring_transaction_id,
            obj.two_to_one_transaction_id,
            obj.online_transaction_id,
            obj.group_transaction_id,
            obj.company_transaction_id,
        ])
        if not has_transaction:
            return None
        return CSTransactionSummarySerializer(obj).data

