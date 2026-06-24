import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from class_scheduling.models import ScheduledClass
from client_school_group_attendance.models import (
    GroupClassMeetingRecord,
    GroupClassStudentAttendanceRecord,
)
from client_school_group_attendance.serializers import (
    GroupClassMeetingRecordSerializer,
    GroupClassStudentAttendanceRecordUpdateSerializer,
    GroupClassStudentAttendanceRecordSerializer,
)
from client_school_group_attendance.utils import (
    handle_group_class_attendance_hours_modification,
)


class GroupClassMeetingRecordRetrieveView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, scheduled_class_id, *args, **kwargs):
        scheduled_class = get_object_or_404(
            ScheduledClass, id=scheduled_class_id
        )
        meeting_record = get_object_or_404(
            GroupClassMeetingRecord,
            scheduled_class=scheduled_class
        )
        serializer = GroupClassMeetingRecordSerializer(meeting_record)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupClassStudentAttendanceBulkUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        attendance_records_data = request.data.get('attendance_records', [])
        if not attendance_records_data:
            return Response(
                {'error': 'No attendance records provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_records = []
        errors = []
        hours_modification_messages = []

        for record_data in attendance_records_data:
            record_id = record_data.get('id')
            attendance_record = get_object_or_404(
                GroupClassStudentAttendanceRecord, id=record_id
            )
            previous_status = attendance_record.attendance_status
            serializer = GroupClassStudentAttendanceRecordUpdateSerializer(
                attendance_record, data=record_data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                modification_message = handle_group_class_attendance_hours_modification(
                    attendance_record=attendance_record,
                    previous_status=previous_status,
                )
                if modification_message:
                    hours_modification_messages.append(modification_message)
                updated_records.append(serializer.data)
            else:
                errors.append({
                    'id': record_id,
                    'errors': serializer.errors
                })

        if errors:
            return Response(
                {
                    'updated_records': updated_records,
                    'errors': errors,
                    'hours_modification_messages': hours_modification_messages,
                },
                status=status.HTTP_207_MULTI_STATUS
            )

        return Response(
            {
                'updated_records': updated_records,
                'hours_modification_messages': hours_modification_messages,
            },
            status=status.HTTP_200_OK
        )


class GroupClassAttendanceByStudentAndClassNameFromDateViewSet(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = GroupClassStudentAttendanceRecord.objects.all()
    serializer_class = GroupClassStudentAttendanceRecordSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model

    def get_queryset(self):
        date_str = self.kwargs.get("date")
        group_class_name = self.kwargs.get("group_class_name")
        client_student_name = self.kwargs.get("client_student_name")

        date_list = date_str.split('-')
        date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

        queryset = self.model.objects.filter(
            group_class_meeting_record__class_date__gt=date,
            group_class_meeting_record__group_class__group_class_name=group_class_name,
            student_account__client_student_name=client_student_name,
        ).filter(
            Q(attendance_status='completed') | Q(attendance_status='same_day_cancellation')
        )

        return queryset.select_related(
            'group_class_meeting_record',
            'group_class_meeting_record__group_class',
            'student_account',
        ).order_by(
            'group_class_meeting_record__class_date',
        )
