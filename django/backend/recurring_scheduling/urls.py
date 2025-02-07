from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import RecurringClassesByTeacherListView, RecurringScheduledClassViewSet

app_name = "recurring_scheduling"

router = DefaultRouter()
router.register(r'recurring-class', RecurringScheduledClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'schedule/by-teacher/', RecurringClassesByTeacherListView.as_view(),
         name='recurring-classes-by-teacher'
        ),    
]