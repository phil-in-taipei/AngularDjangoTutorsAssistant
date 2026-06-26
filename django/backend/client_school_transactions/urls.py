from django.urls import path
from .views import StudentMonthlyReportView


app_name = "client_school_transactions"


urlpatterns = [
    path(
        'report/<str:client_student_name>/<int:year>/<int:month>/',
        StudentMonthlyReportView.as_view(),
        name='student-monthly-report'
    ),
]
