from django.contrib import admin

from .models import FreelanceTuitionTransactionRecord, PurchasedHoursModificationRecord

admin.site.register(FreelanceTuitionTransactionRecord)

admin.site.register(PurchasedHoursModificationRecord)