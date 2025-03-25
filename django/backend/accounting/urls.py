from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FreelanceTuitionTransactionViewSet, 
    PurchasedHoursModificationRecordsListViewByAccountAndMonth
)

app_name = "accounting"

router = DefaultRouter()
router.register(r'tuition-transactions', FreelanceTuitionTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'purchased-hours-modifications/by-month-and-account/<int:month>/<int:year>/<int:account_id>/',
        PurchasedHoursModificationRecordsListViewByAccountAndMonth.as_view(),
        name='purchased-hours-modifications-by-month-and-account'
    ),
]