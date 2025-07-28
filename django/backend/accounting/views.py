from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profiles.models import UserProfile
from school.models import School

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
    generate_estimated_earnings_report,
    generate_estimated_monthly_earnings_report_for_single_school,
    generate_estimated_earnings_report_for_single_school_within_date_range,
    generate_and_email_school_monthly_earnings_report_file
)


class EstimatedEarningsByMonthAndYear(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, *args, **kwargs):
        teacher = get_object_or_404(UserProfile, user=self.request.user)
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        monthly_accounting_report = generate_estimated_earnings_report(
            teacher=teacher, month=month, year=year
        )
        
        return Response(monthly_accounting_report)


class EstimatedSchoolEarningsByMonthAndYear(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, *args, **kwargs):
        school_id = self.kwargs.get("school_id")
        school = get_object_or_404(School, id=school_id)
        teacher = get_object_or_404(UserProfile, user=self.request.user)
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        monthly_accounting_report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=teacher, school=school, month=month, year=year
        )
        
        return Response(monthly_accounting_report)



# this will send an excel file with the monthly report formated
# so that each students'/class' data will be sorted by duration
# to match the accounting report format used at my current job
class EstimatedSchoolEarningsEmailReportByMonthAndYear(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, *args, **kwargs):
        school_id = self.kwargs.get("school_id")
        school = get_object_or_404(School, id=school_id)
        teacher = get_object_or_404(UserProfile, user=self.request.user)
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        try:
            data = generate_and_email_school_monthly_earnings_report_file(
                    teacher=teacher, school=school, 
                    month=month, year=year
                )
            print("-------------------------------------------------------------")
            #print(data)
            return Response({"message": "Data Recieved"}
            )
        except Exception as e:
            return Response(
                {"Error": "There was an error generating the report"},
                status=status.HTTP_400_BAD_REQUEST
            )



class EstimatedSchoolEarningsWithinDateRange(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, *args, **kwargs):
        school_id = self.kwargs.get("school_id")
        school = get_object_or_404(School, id=school_id)
        teacher = get_object_or_404(UserProfile, user=self.request.user)
        start_date = self.kwargs.get("start_date")
        finish_date = self.kwargs.get("finish_date")
        accounting_report_within_date_range = generate_estimated_earnings_report_for_single_school_within_date_range(
            teacher=teacher, school=school, 
            start_date=start_date, finish_date=finish_date
        )
        
        return Response(accounting_report_within_date_range)


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
        previous_hours_purchased = student_or_class.purchased_class_hours
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
            'time_stamp',
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
            'time_stamp',
        )
