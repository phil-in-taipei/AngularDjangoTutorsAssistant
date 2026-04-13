from staff_admin.sites import staff_admin_site
from datetime import time, timedelta, datetime
from django import forms
from django.contrib import admin, messages
from rangefilter.filters import DateRangeFilter

from .models import ScheduledClass, CLASS_STATUS
from .utils import class_is_double_booked
from student_account.models import StudentOrClass


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


def get_duration_from_times(start_time: time, finish_time: time) -> str | None:
    """
    Reverse-calculates the duration string from start and finish times,
    accounting for the -1 minute adjustment used in calculate_finish_time.
    Returns a DURATION_OPTIONS key string like '1,30', or None if no match.
    """
    start_dt = datetime.combine(datetime.today(), start_time)
    finish_dt = datetime.combine(datetime.today(), finish_time)
    actual_minutes = int((finish_dt - start_dt).total_seconds() / 60) + 1  # re-add the 1 min

    hours, minutes = divmod(actual_minutes, 60)
    candidate = f"{hours},{minutes}"

    valid_keys = {opt[0] for opt in DURATION_OPTIONS}
    return candidate if candidate in valid_keys else None


class ClassStatusFilter(admin.SimpleListFilter):
    title = 'class status'
    parameter_name = 'class_status'

    def lookups(self, request, model_admin):
        return CLASS_STATUS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(class_status=self.value())
        return queryset


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
            return queryset.filter(start_time__lt=time(12, 0))
        if self.value() == 'afternoon':
            return queryset.filter(
                start_time__gte=time(12, 0), start_time__lt=time(17, 0)
            )
        if self.value() == 'evening':
            return queryset.filter(start_time__gte=time(17, 0))
        return queryset


class StaffScheduledClassForm(forms.ModelForm):
    duration = forms.ChoiceField(
        choices=DURATION_OPTIONS,
        required=True,
        label='Duration',
        help_text='The finish time will be calculated automatically.'
    )

    class Meta:
        model = ScheduledClass
        fields = (
            'student_or_class', 'date', 'start_time', 'duration', 'location',
            'class_status', 'teacher_notes', 'class_content', 
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

        # When editing an existing instance, pre-select the correct duration
        instance = kwargs.get('instance')
        if instance and instance.pk and instance.start_time and instance.finish_time:
            matched_duration = get_duration_from_times(instance.start_time, instance.finish_time)
            if matched_duration:
                self.fields['duration'].initial = matched_duration


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        duration = cleaned_data.get('duration')

        if start_time and duration:
            cleaned_data['finish_time'] = calculate_finish_time(start_time, duration)

        return cleaned_data


class StaffScheduledClassAdmin(admin.ModelAdmin):
    form = StaffScheduledClassForm
    autocomplete_fields = ['student_or_class']
    exclude = ('teacher', 'finish_time')  # hides the field from the form
    list_display = ('teacher', 'student_or_class', 'date',
                    'start_time', 'finish_time', 'location')
    ordering = ('-date', 'teacher__given_name', 'start_time')
    list_filter = (
        ('date', DateRangeFilter),
        StartTimeRangeFilter,
        ClassStatusFilter,
    )
    search_fields = [
        'student_or_class__student_or_class_name', 
        'teacher__user__username', 'location__space_name'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            student_or_class__school__school_name="David's English Center"
        )

    def save_model(self, request, obj, form, change):
        # automatically set teacher from the school's scheduling_teacher
        if not change:
            obj.teacher = obj.student_or_class.school.scheduling_teacher

        classes_booked_on_date = (
            ScheduledClass.custom_query.teacher_already_booked_classes_on_date(
                query_date=obj.date,
                teacher_id=obj.teacher
            )
        )

        if change:
            classes_booked_on_date = classes_booked_on_date.exclude(id=obj.id)

        # finish_time already set on the form instance via clean()
        obj.finish_time = form.cleaned_data['finish_time']

        if class_is_double_booked(
            classes_booked_on_date=classes_booked_on_date,
            starting_time=obj.start_time,
            finishing_time=obj.finish_time
        ):
            self.message_user(
                request,
                "Scheduling conflict — the teacher is unavailable for this time frame.",
                level=messages.ERROR
            )
            return
        
        if obj.location:
            classes_booked_on_date_in_location = (
                ScheduledClass.custom_query.location_already_booked_classes_on_date(
                    query_date=obj.date,
                    location_id=obj.location
                )
            )
            if change:
                classes_booked_on_date_in_location = classes_booked_on_date_in_location.exclude(id=obj.id)
            if class_is_double_booked(
                classes_booked_on_date=classes_booked_on_date_in_location,
                starting_time=obj.start_time,
                finishing_time=obj.finish_time
            ):
                self.message_user(
                    request,
                    "Scheduling conflict — the room is unavailable for this time frame.",
                    level=messages.ERROR
                )
                return


        super().save_model(request, obj, form, change)


staff_admin_site.register(ScheduledClass, StaffScheduledClassAdmin)
