from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import ScheduledClass


class ScheduledClassAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student_or_class', 'date',
                    'start_time', 'finish_time',)
    list_filter = (
        ('date', DateRangeFilter),
    )
    search_fields = [
        'student_or_class__student_or_class_name', 'teacher__user__username'
    ]


admin.site.register(ScheduledClass, ScheduledClassAdmin)
