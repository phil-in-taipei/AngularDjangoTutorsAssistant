from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FreelanceTuitionTransactionViewSet

app_name = "accounting"

router = DefaultRouter()
router.register(r'tuition-transactions', FreelanceTuitionTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]