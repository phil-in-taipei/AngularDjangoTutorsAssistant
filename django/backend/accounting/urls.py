from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EstimatedEarningsByMonthAndYear,
    FreelanceTuitionTransactionsListViewByMonthAndYear,
    FreelanceTuitionTransactionViewSet,
    PurchasedHoursModificationRecordsListViewByAccountAndMonth
)

app_name = "accounting"

router = DefaultRouter()
router.register(r'tuition-transactions', FreelanceTuitionTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('estimated-earnings-by-month-year/<int:month>/<int:year>/',
         EstimatedEarningsByMonthAndYear.as_view(),
         name='estimated-earnings-by-month-year'
    ),
    path(
        'purchased-hours-modifications/by-month-and-account/<int:month>/<int:year>/<int:account_id>/',
        PurchasedHoursModificationRecordsListViewByAccountAndMonth.as_view(),
        name='purchased-hours-modifications-by-month-and-account'
    ),
    path(
        'received-tuition-transactions-by-month-year/<int:month>/<int:year>/',
        FreelanceTuitionTransactionsListViewByMonthAndYear.as_view(),
        name='received-payments-by-month-year'
    ),
]