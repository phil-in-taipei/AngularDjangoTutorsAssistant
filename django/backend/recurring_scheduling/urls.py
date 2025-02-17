from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    RecurringClassAppliedMonthlyViewSet, 
    RecurringClassAppliedMonthlyListView,
    RecurringClassesByTeacherListView, 
    RecurringScheduledClassViewSet
)

app_name = "recurring_scheduling"

router = DefaultRouter()
router.register(r'recurring-class', RecurringScheduledClassViewSet)
router.register(r'applied-monthly', RecurringClassAppliedMonthlyViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'monthly/recurring/by-teacher/<int:month>/<int:year>/',
        RecurringClassAppliedMonthlyListView.as_view(),
        name='recurring-applied-monthly-by-teacher'
    ),
    path(
        'schedule/by-teacher/', RecurringClassesByTeacherListView.as_view(),
         name='recurring-classes-by-teacher'
        ),    
]