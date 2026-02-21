#from django.contrib import admin

#from .models import RecurringScheduledClass, RecurringClassAppliedMonthly

#admin.site.register(RecurringScheduledClass)
#admin.site.register(RecurringClassAppliedMonthly)

from django.contrib import admin
from django.contrib import messages

from .models import RecurringScheduledClass, RecurringClassAppliedMonthly
from .utils import (
    create_date_list,
    recurring_class_applied_monthly_has_scheduling_conflict,
    book_classes_for_specified_month,
)


class RecurringScheduledClassAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student_or_class', 'day_of_week_string',
                    'recurring_start_time', 'recurring_finish_time',)
    list_filter = ('recurring_day_of_week',)
    search_fields = [
        'student_or_class__student_or_class_name', 'teacher__user__username'
    ]


class RecurringClassAppliedMonthlyAdmin(admin.ModelAdmin):
    list_display = ('recurring_class', 'get_teacher', 'get_student_or_class',
                    'scheduling_month', 'scheduling_year',)
    list_filter = ('scheduling_month', 'scheduling_year',
                   'recurring_class__recurring_day_of_week',)
    search_fields = [
        'recurring_class__student_or_class__student_or_class_name',
        'recurring_class__teacher__user__username'
    ]

    def get_teacher(self, obj):
        return obj.recurring_class.teacher
    get_teacher.short_description = 'Teacher'
    get_teacher.admin_order_field = 'recurring_class__teacher__user__username'

    def get_student_or_class(self, obj):
        return obj.recurring_class.student_or_class
    get_student_or_class.short_description = 'Student or Class'
    get_student_or_class.admin_order_field = 'recurring_class__student_or_class__student_or_class_name'

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        monthly_booking_date_list = create_date_list(
            year=obj.scheduling_year,
            month=obj.scheduling_month,
            day_of_week=obj.recurring_class.recurring_day_of_week
        )

        if recurring_class_applied_monthly_has_scheduling_conflict(
            list_of_dates_on_day_in_given_month=monthly_booking_date_list,
            recurring_class=obj.recurring_class
        ):
            self.message_user(
                request,
                "Scheduling conflict detected — recurring class was not applied.",
                level=messages.ERROR
            )
            return

        super().save_model(request, obj, form, change)
        book_classes_for_specified_month(
            date_list=monthly_booking_date_list,
            recurring_class=obj.recurring_class
        )
        self.message_user(
            request,
            "Recurring class applied successfully.",
            level=messages.SUCCESS
        )


admin.site.register(RecurringScheduledClass, RecurringScheduledClassAdmin)
admin.site.register(RecurringClassAppliedMonthly, RecurringClassAppliedMonthlyAdmin)

