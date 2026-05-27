from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import (
    AccountingClientSchoolStudentAccount,
    AccountingClientSchoolGroupClass,
    ClientSchoolClassEnrollmentHandler,
)

DAVIDS_ENGLISH = "David's English Center"


class AccountingClientSchoolStudentAccountAdmin(admin.ModelAdmin):
    list_display = (
        'client_student_name',
        'client_school',
        'student_level',
        'purchased_tutoring_hours',
        'tutoring_hours_expiration_date',
        'purchased_group_class_hours',
        'group_hours_expiration_date',
        'purchased_online_hours',
        'online_hours_expiration_date',
        'purchased_company_hours',
        'company_hours_expiration_date',
    )
    search_fields = (
        'client_student_name',
        'client_school__school_name',
    )
    list_filter = (
        'client_school',
        'student_level',
    )
    ordering = ('client_school__school_name', 'client_student_name')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            client_school__school_name=DAVIDS_ENGLISH
        )


class AccountingClientSchoolGroupClassAdmin(admin.ModelAdmin):
    list_display = (
        'group_class_name',
        'client_school',
        'student_level',
    )
    search_fields = (
        'group_class_name',
        'client_school__school_name',
    )
    list_filter = (
        'client_school',
        'student_level',
    )
    ordering = ('client_school__school_name', 'group_class_name')
    filter_horizontal = ('client_group_class_accounts',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            client_school__school_name=DAVIDS_ENGLISH
        )

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(
                request,
                f"Validation error: {e.message}",
                level=messages.ERROR
            )


class ClientSchoolClassEnrollmentHandlerAdmin(admin.ModelAdmin):
    list_display = (
        'student_or_class',
        'class_enrollment_type',
        'client_school_one_to_one_account',
        'client_school_online_account',
        'client_school_company_account',
        'client_group_class',
    )
    search_fields = (
        'student_or_class__student_or_class_name',
        'student_or_class__teacher__surname',
        'student_or_class__teacher__given_name',
        'client_school_one_to_one_account__client_student_name',
        'client_school_online_account__client_student_name',
        'client_school_company_account__client_student_name',
        'client_group_class__group_class_name',
    )
    list_filter = (
        'class_enrollment_type',
    )
    ordering = (
        'student_or_class__teacher__surname',
        'class_enrollment_type',
    )
    filter_horizontal = ('client_school_two_to_one_accounts',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            student_or_class__school__school_name=DAVIDS_ENGLISH
        )

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(
                request,
                f"Validation error: {e.message}",
                level=messages.ERROR
            )


admin.site.register(
    AccountingClientSchoolStudentAccount,
    AccountingClientSchoolStudentAccountAdmin
)
admin.site.register(
    AccountingClientSchoolGroupClass,
    AccountingClientSchoolGroupClassAdmin
)
admin.site.register(
    ClientSchoolClassEnrollmentHandler,
    ClientSchoolClassEnrollmentHandlerAdmin
)
