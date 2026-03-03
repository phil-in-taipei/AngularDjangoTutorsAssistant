from staff_admin.sites import staff_admin_site
from datetime import time
from django import forms
from django.contrib import admin, messages
from rangefilter.filters import DateRangeFilter

from .models import ScheduledClass
from .utils import class_is_double_booked
from student_account.models import StudentOrClass


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
    class Meta:
        model = ScheduledClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_or_class'].queryset = StudentOrClass.objects.filter(
            school__school_name="David's English Center"
        ).order_by(
            'teacher__surname',
            'teacher__given_name',
            'student_or_class_name'
        )


class StaffScheduledClassAdmin(admin.ModelAdmin):
    form = StaffScheduledClassForm
    exclude = ('teacher',)  # hides the field from the form
    list_display = ('teacher', 'student_or_class', 'date',
                    'start_time', 'finish_time',)
    list_filter = (
        ('date', DateRangeFilter),
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

        super().save_model(request, obj, form, change)


staff_admin_site.register(ScheduledClass, StaffScheduledClassAdmin)
