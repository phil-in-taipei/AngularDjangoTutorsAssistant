import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from accounting.utils import create_timestamps_for_beginning_and_end_of_month_and_year
from client_school_accounting.models import (
    AccountingClientSchoolStudentAccount,
    ClientSchoolClassEnrollmentHandler,
)
from client_school_group_attendance.serializers import (
    GroupClassStudentAttendanceRecordSerializer,
)
from client_school_group_attendance.models import GroupClassStudentAttendanceRecord
from class_scheduling.models import ScheduledClass
from class_scheduling.serializers import ScheduledClassGoogleCalendarSerializer
from .models import CSPurchasedHoursModification
from .serializers import (
    CSPurchasedHoursModificationSerializer,
)


class StudentMonthlyReportView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, client_student_name, year, month):
        # --- Validate year/month ---
        try:
            year = int(year)
            month = int(month)
            # Confirm it's a real month
            datetime.date(year, month, 1)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid year or month.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- Resolve the student account ---
        # If you want to scope by school, add &client_school=... as a query param
        # or add school_id to the URL. For now, match on name alone.
        student_account = get_object_or_404(
            AccountingClientSchoolStudentAccount,
            client_student_name=client_student_name,
        )

        query_timestamps = create_timestamps_for_beginning_and_end_of_month_and_year(
            month=month,
            year=year
        )

        # --- Account activity: all hours modifications for this month ---
        modifications = CSPurchasedHoursModification.objects.filter(
            student_account=student_account,
            time_stamp__range=(query_timestamps['start'], query_timestamps['end']),
        ).select_related(
            'bridge',
            'tutoring_transaction',
            'two_to_one_transaction',
            'online_transaction',
            'group_transaction',
            'company_transaction',
        ).order_by('time_stamp')

        # --- Group class attendance for this month ---
        group_attendance = GroupClassStudentAttendanceRecord.objects.filter(
            student_account=student_account,
            group_class_meeting_record__class_date__year=year,
            group_class_meeting_record__class_date__month=month,
        ).select_related(
            'group_class_meeting_record',
            'group_class_meeting_record__group_class',
            'student_account',
        ).order_by('group_class_meeting_record__class_date')

        # --- Individual class attendance (tutoring, online, company) ---
        # Navigate: student_account -> enrollment handlers -> StudentOrClass -> ScheduledClass
        enrollment_handlers = ClientSchoolClassEnrollmentHandler.objects.filter(
            Q(client_school_one_to_one_account=student_account)
            | Q(client_school_two_to_one_accounts=student_account)
            | Q(client_school_online_account=student_account)
            | Q(client_school_company_account=student_account)
        ).select_related('student_or_class')

        student_or_class_ids = enrollment_handlers.values_list(
            'student_or_class_id', flat=True
        )

        individual_classes = ScheduledClass.objects.filter(
            student_or_class_id__in=student_or_class_ids,
            date__year=year,
            date__month=month,
        ).filter(
            Q(class_status='completed') | Q(class_status='same_day_cancellation')
        ).select_related(
            'teacher',
            'student_or_class',
            'location',
        ).order_by('date', 'start_time')

        # --- Current balances snapshot ---
        balances = {}
        for field, label in [
            ('purchased_tutoring_hours', 'tutoring'),
            ('purchased_group_class_hours', 'group_class'),
            ('purchased_online_hours', 'online'),
            ('purchased_company_hours', 'company'),
        ]:
            val = getattr(student_account, field)
            if val is not None:
                balances[label] = float(val)

        # --- Serialize and return ---
        return Response({
            'student_name': student_account.client_student_name,
            'report_period': {
                'year': year,
                'month': month,
            },
            'current_balances': balances,
            'account_activity': CSPurchasedHoursModificationSerializer(
                modifications, many=True
            ).data,
            'group_class_attendance': GroupClassStudentAttendanceRecordSerializer(
                group_attendance, many=True
            ).data,
            'individual_class_attendance': ScheduledClassGoogleCalendarSerializer(
                individual_classes, many=True
            ).data,
        })
