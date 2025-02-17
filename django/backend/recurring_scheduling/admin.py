from django.contrib import admin

from .models import RecurringScheduledClass, RecurringClassAppliedMonthly

admin.site.register(RecurringScheduledClass)
admin.site.register(RecurringClassAppliedMonthly)
