from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ScheduledClassViewSet, ScheduledClassByTeacherByMonthViewSet

app_name = "class_scheduling"

router = DefaultRouter()
router.register(r'class/submit', ScheduledClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'classes/by-teacher/by-month-year/<int:month>/<int:year>/',
        ScheduledClassByTeacherByMonthViewSet.as_view(),
        name='class-scheduling-by-teacher-month-year'
    ),
]
