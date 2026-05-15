from django.contrib import admin

from .models import (
    ClientSchoolTutoringTuitionTransactionRecord, 
    ClientSchool2to1TutoringTuitionTransactionRecord
)

admin.site.register(ClientSchoolTutoringTuitionTransactionRecord)
admin.site.register(ClientSchool2to1TutoringTuitionTransactionRecord)

