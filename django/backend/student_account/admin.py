from django.contrib import admin

from .models import StudentOrClass


class StudentOrClassAdmin(admin.ModelAdmin):
    list_display = (
        'teacher', 'student_or_class_name',
        'account_type', 'school',
        'purchased_class_hours',
    )

    search_fields = (
        'teacher__user__username', 'teacher__surname',
        'teacher__given_name','school__school_name'
    )


admin.site.register(StudentOrClass, StudentOrClassAdmin)




