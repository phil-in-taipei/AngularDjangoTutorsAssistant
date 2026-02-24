#from django.contrib import admin
#from rangefilter.filters import DateRangeFilter
#from .models import ScheduledClass


#class ScheduledClassAdmin(admin.ModelAdmin):
#    list_display = ('teacher', 'student_or_class', 'date',
#                    'start_time', 'finish_time',)
#    list_filter = (
#        ('date', DateRangeFilter),
#    )
#    search_fields = [
#        'student_or_class__student_or_class_name', 'teacher__user__username'
#    ]


#admin.site.register(ScheduledClass, ScheduledClassAdmin)

from django.contrib import admin
from django.contrib import messages
from rangefilter.filters import DateRangeFilter

from .models import ScheduledClass
from .utils import class_is_double_booked  # adjust import path as needed


class ScheduledClassAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student_or_class', 'date',
                    'start_time', 'finish_time',)
    list_filter = (
        ('date', DateRangeFilter),
    )
    search_fields = [
        'student_or_class__student_or_class_name', 'teacher__user__username'
    ]

    def save_model(self, request, obj, form, change):
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


admin.site.register(ScheduledClass, ScheduledClassAdmin)
