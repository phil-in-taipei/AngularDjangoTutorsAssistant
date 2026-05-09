from django.contrib import admin

from .models import AccountingClientSchoolStudentAccount


class AccountingClientSchoolStudentAccountAdmin(admin.ModelAdmin):
    list_display = (
        'client_student_name', 'client_school',
        'student_level', 'purchased_group_class_hours',
        'purchased_tutoring_hours',
    )

    search_fields = (
        'client_student_name', 'student_level',
        'client_school__school_name', 
    )


admin.site.register(
    AccountingClientSchoolStudentAccount, 
    AccountingClientSchoolStudentAccountAdmin
)