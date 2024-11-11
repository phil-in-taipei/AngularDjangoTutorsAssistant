from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (ScheduledClassStatusConfirmationViewSet,
                    ScheduledClassViewSet, ScheduledClassByTeacherByDateViewSet,
                    ScheduledClassByTeacherByMonthViewSet, UnconfirmedStatusClassesViewSet)

app_name = "class_scheduling"

router = DefaultRouter()
router.register(r'class/submit', ScheduledClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
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
        'class-status-confirmation/',
        ScheduledClassStatusConfirmationViewSet.as_view(),
        name='class-status-confirmation'
    ),
    path(
        'classes/unconfirmed-status/',
        UnconfirmedStatusClassesViewSet.as_view(),
        name='classes-unconfirmed'
    ),
]
