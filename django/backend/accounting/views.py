from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profiles.models import UserProfile
from .models import (
    FreelanceTuitionTransactionRecord,
    PurchasedHoursModificationRecord
    )
from .serializers import (
    FreelanceTuitionTransactionRecordSerializer, 
    PurchasedHoursModificationRecordSerializer
    )
from .utils import (
    create_purchased_hours_modification_record_for_tuition_transaction,
    create_timestamps_for_beginning_and_end_of_month_and_year,
    generate_estimated_earnings_report
    )


class EstimatedEarningsByMonthAndYear(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, *args, **kwargs):
        query_list = []
        teacher = get_object_or_404(UserProfile, user=self.request.user)
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        query_list = generate_estimated_earnings_report(teacher=teacher, month=month, year=year)
        print("will return this.....")
        print(query_list)
        print("*************************************************")
        return Response(query_list)

class FreelanceTuitionTransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated, #IsOwnerOrReadOnly
    )
    queryset = FreelanceTuitionTransactionRecord.objects.all()
    serializer_class = FreelanceTuitionTransactionRecordSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_or_class = serializer.validated_data['student_or_class']
        #student_or_class = get_object_or_404(StudentOrClass, id=student_or_class_id)
        previous_hours_purchased = student_or_class.purchased_class_hours
        #previous_hours_purchased, freelance_tuition_transaction_record
        freelance_tuition_transaction=serializer.save()
        create_purchased_hours_modification_record_for_tuition_transaction(
                previous_hours_purchased=previous_hours_purchased, 
                freelance_tuition_transaction_record=freelance_tuition_transaction
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FreelanceTuitionTransactionsListViewByMonthAndYear(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = FreelanceTuitionTransactionRecord.objects.all()
    serializer_class = FreelanceTuitionTransactionRecordSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model

    def get_queryset(self):
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        query_timestamps = create_timestamps_for_beginning_and_end_of_month_and_year(
            month, year
        )

        queryset = self.model.objects.filter(
            student_or_class__teacher__user=self.request.user,
            time_stamp__range=(query_timestamps['start'], query_timestamps['end'])
        )
        return queryset.order_by(
            '-time_stamp',
        )


class PurchasedHoursModificationRecordsListViewByAccountAndMonth(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = PurchasedHoursModificationRecord.objects.all()
    serializer_class = PurchasedHoursModificationRecordSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model

    def get_queryset(self):
        print("***********getting the query now********")
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        account_id = self.kwargs.get("account_id")
        query_timestamps = create_timestamps_for_beginning_and_end_of_month_and_year(
            month, year
        )

        queryset = self.model.objects.filter(
            student_or_class__id=account_id,
            time_stamp__range=(query_timestamps['start'], query_timestamps['end'])
        )
        return queryset.order_by(
            '-time_stamp',
        )