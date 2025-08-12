from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ScheduledClassStatusConfirmationViewSet,
    ScheduledClassBatchDeletionView,
    ScheduledClassViewSet,
    ScheduledClassByTeacherByDateViewSet,
    ScheduledClassByTeacherByMonthViewSet,
    ScheduledClassGoogleCalendarViewSet,
    StudentOrClassAttendanceViewSet,
    UnconfirmedStatusClassesViewSet
)

app_name = "class_scheduling"

router = DefaultRouter()
router.register(r'class/submit', ScheduledClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'classes/batch-delete/',
        ScheduledClassBatchDeletionView.as_view(),
        name='class-batch-delete'
    ),
    path(
        'classes/by-teacher/by-date/<str:date>/',
        ScheduledClassByTeacherByDateViewSet.as_view(),
        name='class-scheduling-by-teacher-by-date'
    ),
    path(
        'classes/by-teacher/by-month-year/<int:month>/<int:year>/',
        ScheduledClassByTeacherByMonthViewSet.as_view(),
        name='class-scheduling-by-teacher-month-year'
    ),
    path(
        'classes/google-calendar/by-month-year/<int:month>/<int:year>/',
        ScheduledClassGoogleCalendarViewSet.as_view(),
        name='class-scheduling-google-calendar'
    ),
    path(
        'class-status-confirmation/',
        ScheduledClassStatusConfirmationViewSet.as_view(),
        name='class-status-confirmation'
    ),
    path(
        'classes/student-or-class-attendance/<int:student_or_class_id>/',
        StudentOrClassAttendanceViewSet.as_view(), name='student-or-class-attendance'
    ),
    path(
        'classes/unconfirmed-status/',
        UnconfirmedStatusClassesViewSet.as_view(),
        name='classes-unconfirmed'
    ),
]
