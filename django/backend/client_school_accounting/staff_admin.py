from staff_admin.sites import staff_admin_site
from django.contrib import admin


from client_school_accounting.models import AccountingClientSchoolStudentAccount


class StaffAccountingClientSchoolStudentAccountAdmin(admin.ModelAdmin):
    list_display = (
        'client_student_name', 'client_school',
        'student_level', 'purchased_group_class_hours',
        'purchased_tutoring_hours',
    )

    search_fields = (
        'client_student_name', 'student_level',
        'client_school__school_name',
    )



staff_admin_site.register( 
    AccountingClientSchoolStudentAccount, 
    StaffAccountingClientSchoolStudentAccountAdmin
)
