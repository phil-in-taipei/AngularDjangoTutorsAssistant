from staff_admin.sites import staff_admin_site
from datetime import time, timedelta, datetime
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



DURATION_OPTIONS = [
    ('0,30',  '30 mins'),
    ('0,45',  '45 mins'),
    ('1,0',   '1 hr'),
    ('1,15',  '1 hr 15 mins'),
    ('1,30',  '1 hr 30 mins'),
    ('1,45',  '1 hr 45 mins'),
    ('2,0',   '2 hrs'),
    ('2,15',  '2 hrs 15 mins'),
    ('2,30',  '2 hrs 30 mins'),
    ('2,45',  '2 hrs 45 mins'),
    ('3,0',   '3 hrs'),
    ('3,15',  '3 hrs 15 mins'),
    ('3,30',  '3 hrs 30 mins'),
    ('3,45',  '3 hrs 45 mins'),
    ('4,0',   '4 hrs'),
    ('4,15',  '4 hrs 15 mins'),
    ('4,30',  '4 hrs 30 mins'),
    ('4,45',  '4 hrs 45 mins'),
    ('5,0',   '5 hrs'),
]


def calculate_finish_time(start_time: time, duration_str: str) -> time:
    """
    Calculates the finish time from a start time and duration string.
    Subtracts 1 minute from the total duration to avoid double-booking conflicts,
    mirroring the logic used on the Angular front end.

    Args:
        start_time: A datetime.time object for the class start time.
        duration_str: A string in the format "hours,minutes" e.g. "1,30".

    Returns:
        A datetime.time object for the finish time.
    """
    hours, minutes = map(int, duration_str.split(','))
    total_minutes = (hours * 60) + minutes - 1  # subtract 1 to avoid overlap
    start_dt = datetime.combine(datetime.today(), start_time)
    finish_dt = start_dt + timedelta(minutes=total_minutes)
    return finish_dt.time()



class StartTimeRangeFilter(admin.SimpleListFilter):
    title = 'start time'
    parameter_name = 'start_time_range'

    def lookups(self, request, model_admin):
        # These are the "quick-select" options that will appear in the sidebar
        return (
            ('morning', 'Morning (Before 12:00)'),
            ('afternoon', 'Afternoon (12:00 - 17:00)'),
            ('evening', 'Evening (After 17:00)'),
        )

    def queryset(self, request, queryset):
        """
        Applies the filtering logic based on the selection.
        """
        if self.value() == 'morning':
            return queryset.filter(recurring_start_time__lt=time(12, 0))
        if self.value() == 'afternoon':
            return queryset.filter(
                recurring_start_time__gte=time(12, 0), recurring_start_time__lt=time(17, 0)
            )
        if self.value() == 'evening':
            return queryset.filter(recurring_start_time__gte=time(17, 0))
        return queryset


class StaffRecurringScheduledClassForm(forms.ModelForm):
    duration = forms.ChoiceField(
        choices=DURATION_OPTIONS,
        required=True,
        label='Duration',
        help_text='The finish time will be calculated automatically.'
    )

    class Meta:
        model = RecurringScheduledClass
        fields = (
            'student_or_class', 'recurring_day_of_week', 
            'recurring_start_time', 'duration',
            )
        # finish_time is excluded — it will be set in clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_or_class'].queryset = StudentOrClass.objects.filter(
            school__school_name="David's English Center"
        ).order_by(
            'teacher__surname',
            'teacher__given_name',
            'student_or_class_name'
        )

    
    def clean(self):
        cleaned_data = super().clean()
        recurring_start_time = cleaned_data.get('recurring_start_time')
        duration = cleaned_data.get('duration')

        if recurring_start_time and duration:
            cleaned_data['recurring_finish_time'] = calculate_finish_time(recurring_start_time, duration)

        return cleaned_data


class StaffRecurringScheduledClassAdmin(admin.ModelAdmin):
    form = StaffRecurringScheduledClassForm
    exclude = ('teacher', 'recurring_finish_time')  # hides the field from the form
    autocomplete_fields = ['student_or_class']
    list_display = ('teacher', 'student_or_class', 'day_of_week_string',
                    'recurring_start_time', 'recurring_finish_time',)
    list_filter = (
            'recurring_day_of_week',
            StartTimeRangeFilter,
        )
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
                # finish_time already set on the form instance via clean()
        obj.recurring_finish_time = form.cleaned_data['recurring_finish_time']
        super().save_model(request, obj, form, change)


class StaffRecurringClassAppliedMonthlyForm(forms.ModelForm):
    class Meta:
        model = RecurringClassAppliedMonthly
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'recurring_class' in self.fields:
            self.fields['recurring_class'].queryset = RecurringScheduledClass.objects.filter(
                student_or_class__school__school_name="David's English Center"
            ).order_by(
                'teacher__surname',
                'teacher__given_name',
                'recurring_day_of_week',
                'recurring_start_time'
            )


class StaffRecurringClassAppliedMonthlyAdmin(admin.ModelAdmin):
    form = StaffRecurringClassAppliedMonthlyForm
    autocomplete_fields = ['recurring_class']
    list_display = ('recurring_class', 'get_teacher', 'get_student_or_class',
                    'scheduling_month', 'scheduling_year',)
    list_filter = ('scheduling_month', 'scheduling_year',
                   'recurring_class__recurring_day_of_week',)
    search_fields = [
        'recurring_class__student_or_class__student_or_class_name',
        'recurring_class__teacher__user__username'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            recurring_class__student_or_class__school__school_name="David's English Center"
        )

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