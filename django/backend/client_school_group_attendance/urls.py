from django.urls import path
from client_school_group_attendance.views import (
    GroupClassMeetingRecordRetrieveView,
    GroupClassStudentAttendanceBulkUpdateView,
    GroupClassAttendanceByStudentAndClassNameFromDateViewSet,
)

urlpatterns = [
    path(
        'group-class-meeting-record/<int:scheduled_class_id>/',
        GroupClassMeetingRecordRetrieveView.as_view(),
        name='group-class-meeting-record-retrieve',
    ),
    path(
        'group-class-attendance-bulk-update/',
        GroupClassStudentAttendanceBulkUpdateView.as_view(),
        name='group-class-attendance-bulk-update',
    ),
    path(
        'group-classes/confirmed-since-date/by-student-account/<str:date>/<str:group_class_name>/<str:client_student_name>/',
        GroupClassAttendanceByStudentAndClassNameFromDateViewSet.as_view(),
        name='group-class-attendance-by-student-from-date'
    ),
]
