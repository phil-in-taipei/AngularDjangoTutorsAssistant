from rest_framework.views import APIView
from rest_framework.response import Response
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

