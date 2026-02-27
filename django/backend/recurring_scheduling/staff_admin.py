from staff_admin.sites import staff_admin_site

from django import forms
from django.contrib import admin
from django.contrib import messages

from student_account.models import StudentOrClass
from .models import RecurringScheduledClass, RecurringClassAppliedMonthly
from .utils import (
    create_date_list,
    recurring_class_applied_monthly_has_scheduling_conflict,
    book_classes_for_specified_month,
)


class StaffRecurringScheduledClassForm(forms.ModelForm):
    class Meta:
        model = RecurringScheduledClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['student_or_class'].queryset = StudentOrClass.objects.filter(
        #    school__school_name="David's English Center"
        #)
        self.fields['student_or_class'].queryset = StudentOrClass.objects.filter(
            school__school_name__icontains="David"
        )


class StaffRecurringScheduledClassAdmin(admin.ModelAdmin):
    form = StaffRecurringScheduledClassForm
    exclude = ('teacher',)  # hides the field from the form

    list_display = ('teacher', 'student_or_class', 'day_of_week_string',
                    'recurring_start_time', 'recurring_finish_time',)
    list_filter = ('recurring_day_of_week',)
    search_fields = [
        'student_or_class__student_or_class_name', 'teacher__user__username'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            student_or_class__school__school_name="David's English Center"
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.teacher = obj.student_or_class.school.scheduling_teacher
        super().save_model(request, obj, form, change)


class StaffRecurringClassAppliedMonthlyForm(forms.ModelForm):
    class Meta:
        model = RecurringClassAppliedMonthly
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['student_or_class'].queryset = StudentOrClass.objects.filter(
        #    school__school_name="David's English Center"
        #)
        self.fields['recurring_class'].queryset = RecurringScheduledClass.objects.filter(
            student_or_class__school__school_name__icontains="David"
        )


class StaffRecurringClassAppliedMonthlyAdmin(admin.ModelAdmin):
    form = StaffRecurringClassAppliedMonthlyForm

    list_display = ('recurring_class', 'get_teacher', 'get_student_or_class',
                    'scheduling_month', 'scheduling_year',)
    list_filter = ('scheduling_month', 'scheduling_year',
                   'recurring_class__recurring_day_of_week',)
    search_fields = [
        'recurring_class__student_or_class__student_or_class_name',
        'recurring_class__teacher__user__username'
    ]

    #def get_queryset(self, request):
    #    return super().get_queryset(request).filter(
    #        recurring_class__student_or_class__school__school_name="David's English Center"
    #    )
    def get_queryset(self, request):
        import logging
        logger = logging.getLogger(__name__)
        qs = super().get_queryset(request).filter(
            recurring_class__student_or_class__school__school_name__icontains="David"
        )
        logger.warning(f"Filtered count: {qs.count()}")
        return qs


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


staff_admin_site.register(RecurringScheduledClass, StaffRecurringScheduledClassAdmin)
staff_admin_site.register(RecurringClassAppliedMonthly, StaffRecurringClassAppliedMonthlyAdmin)