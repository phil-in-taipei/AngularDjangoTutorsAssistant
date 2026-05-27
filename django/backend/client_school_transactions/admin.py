from django import forms
from django.contrib import admin
from django.contrib import messages
from rangefilter.filters import DateRangeFilter

from client_school_accounting.models import AccountingClientSchoolStudentAccount

from client_school_transactions.models import (
    CSTutoringTuitionRecord, 
    CST2To1TutoringTuitionRecord,
    CSOnlineTuitionRecord,
    CSGroupClassTuitionRecord,
    CSCompanyClassTuitionRecord,
    CSPurchasedHoursModification
)

from client_school_transactions.utils import (
    create_modification_record_for_tutoring_transaction,
    create_modification_record_for_two_to_one_transaction,
    create_modification_record_for_online_transaction,
    create_modification_record_for_group_transaction,
    create_modification_record_for_company_transaction,
)


DAVIDS_ENGLISH = "David's English Center"


def davids_english_student_accounts():
    return AccountingClientSchoolStudentAccount.objects.filter(
        client_school__school_name=DAVIDS_ENGLISH
    ).order_by('client_student_name')


# ── Forms ──────────────────────────────────────────────────────────────────────

class ClientSchoolTutoringTuitionTransactionForm(forms.ModelForm):
    class Meta:
        model = CSTutoringTuitionRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_account'].queryset = davids_english_student_accounts()


class ClientSchool2to1TutoringTuitionTransactionForm(forms.ModelForm):
    class Meta:
        model = CST2To1TutoringTuitionRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        accounts = davids_english_student_accounts()
        self.fields['primary_student_account'].queryset = accounts
        self.fields['shared_student_account'].queryset = accounts

    def clean(self):
        cleaned_data = super().clean()
        primary = cleaned_data.get('primary_student_account')
        shared = cleaned_data.get('shared_student_account')
        if primary and shared and primary == shared:
            raise forms.ValidationError(
                'Primary and shared student accounts must be different students.'
            )
        return cleaned_data


class ClientSchoolOnlineTuitionTransactionForm(forms.ModelForm):
    class Meta:
        model = CSOnlineTuitionRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_account'].queryset = davids_english_student_accounts()


class ClientSchoolGroupClassesTuitionTransactionForm(forms.ModelForm):
    class Meta:
        model = CSGroupClassTuitionRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_account'].queryset = davids_english_student_accounts()


class ClientSchoolCompanyClassesTuitionTransactionForm(forms.ModelForm):
    class Meta:
        model = CSCompanyClassTuitionRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_account'].queryset = davids_english_student_accounts()



# ── Model Admins ───────────────────────────────────────────────────────────────

class ClientSchoolTutoringTuitionTransactionAdmin(admin.ModelAdmin):
    form = ClientSchoolTutoringTuitionTransactionForm
    readonly_fields = ('time_stamp',)
    list_display = (
        'student_account', 'transaction_type', 'transaction_amount',
        'class_hours_purchased_or_refunded', 'expiration_period',
        'administrator_name', 'time_stamp'
    )
    ordering = ('-time_stamp',)
    search_fields = [
        'student_account__client_student_name',
        'administrator_name',
    ]
    list_filter = (
        ('time_stamp', DateRangeFilter),
        'transaction_type', 
        'expiration_period'
        )

    def save_model(self, request, obj, form, change):
        previous_hours = obj.student_account.purchased_tutoring_hours
        super().save_model(request, obj, form, change)
        create_modification_record_for_tutoring_transaction(
            previous_hours_purchased=previous_hours,
            tutoring_transaction=obj,
        )


class ClientSchool2to1TutoringTuitionTransactionAdmin(admin.ModelAdmin):
    form = ClientSchool2to1TutoringTuitionTransactionForm
    readonly_fields = ('time_stamp',)
    list_display = (
        'primary_student_account', 'shared_student_account', 'transaction_type',
        'transaction_amount', 'class_hours_purchased_or_refunded',
        'expiration_period', 'administrator_name', 'time_stamp'
    )
    ordering = ('-time_stamp',)
    search_fields = [
        'primary_student_account__client_student_name',
        'shared_student_account__client_student_name',
        'administrator_name',
    ]
    list_filter = (
        ('time_stamp', DateRangeFilter),
        'transaction_type', 'expiration_period'
        )

    def save_model(self, request, obj, form, change):
        previous_hours = obj.primary_student_account.purchased_tutoring_hours
        super().save_model(request, obj, form, change)
        create_modification_record_for_two_to_one_transaction(
            previous_hours_purchased=previous_hours,
            two_to_one_transaction=obj,
        )


class ClientSchoolOnlineTuitionTransactionAdmin(admin.ModelAdmin):
    form = ClientSchoolOnlineTuitionTransactionForm
    readonly_fields = ('time_stamp',)
    list_display = (
        'student_account', 'transaction_type', 'transaction_amount',
        'class_hours_purchased_or_refunded', 'expiration_period',
        'administrator_name', 'time_stamp'
    )
    ordering = ('-time_stamp',)
    search_fields = [
        'student_account__client_student_name',
        'administrator_name',
    ]
    list_filter = (
        ('time_stamp', DateRangeFilter),
        'transaction_type', 'expiration_period'
    )

    def save_model(self, request, obj, form, change):
        previous_hours = obj.student_account.purchased_online_hours
        super().save_model(request, obj, form, change)
        create_modification_record_for_online_transaction(
            previous_hours_purchased=previous_hours,
            online_transaction=obj,
        )


class ClientSchoolGroupClassesTuitionTransactionAdmin(admin.ModelAdmin):
    form = ClientSchoolGroupClassesTuitionTransactionForm
    readonly_fields = ('time_stamp',)
    list_display = (
        'student_account', 'transaction_type', 'transaction_amount',
        'class_hours_purchased_or_refunded', 'expiration_period',
        'administrator_name', 'time_stamp'
    )
    ordering = ('-time_stamp',)
    search_fields = [
        'student_account__client_student_name',
        'administrator_name',
    ]
    list_filter = (
        ('time_stamp', DateRangeFilter),
        'transaction_type', 'expiration_period'
    )

    def save_model(self, request, obj, form, change):
        previous_hours = obj.student_account.purchased_group_class_hours
        super().save_model(request, obj, form, change)
        create_modification_record_for_group_transaction(
            previous_hours_purchased=previous_hours,
            group_transaction=obj,
        )


class ClientSchoolCompanyClassesTuitionTransactionAdmin(admin.ModelAdmin):
    form = ClientSchoolCompanyClassesTuitionTransactionForm
    readonly_fields = ('time_stamp',)
    list_display = (
        'student_account', 'transaction_type', 'transaction_amount',
        'class_hours_purchased_or_refunded', 'expiration_period',
        'administrator_name', 'time_stamp'
    )
    ordering = ('-time_stamp',)
    search_fields = [
        'student_account__client_student_name',
        'administrator_name',
    ]
    list_filter = (
        ('time_stamp', DateRangeFilter),
        'transaction_type',
    )

    def save_model(self, request, obj, form, change):
        previous_hours = obj.student_account.purchased_company_hours
        super().save_model(request, obj, form, change)
        create_modification_record_for_company_transaction(
            previous_hours_purchased=previous_hours,
            company_transaction=obj,
        )


class ClientSchoolPurchasedHoursModificationRecordAdmin(admin.ModelAdmin):
    readonly_fields = (
        'student_account',
        'bridge',
        'class_type',
        'modification_type',
        'tutoring_transaction',
        'two_to_one_transaction',
        'online_transaction',
        'group_transaction',
        'company_transaction',
        'previous_hours',
        'updated_hours',
        'time_stamp',
    )
    list_display = (
        'student_account',
        'class_type',
        'modification_type',
        'previous_hours',
        'updated_hours',
        'time_stamp',
    )
    ordering = ('-time_stamp',)
    search_fields = [
        'student_account__client_student_name',
        'student_account__client_school__school_name',
    ]
    list_filter = (
        ('time_stamp', DateRangeFilter),
        'class_type',
        'modification_type',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ── Registration ───────────────────────────────────────────────────────────────

admin.site.register(
    CSTutoringTuitionRecord,
    ClientSchoolTutoringTuitionTransactionAdmin
)
admin.site.register(
    CST2To1TutoringTuitionRecord,
    ClientSchool2to1TutoringTuitionTransactionAdmin
)
admin.site.register(
    CSOnlineTuitionRecord,
    ClientSchoolOnlineTuitionTransactionAdmin
)
admin.site.register(
    CSGroupClassTuitionRecord,
    ClientSchoolGroupClassesTuitionTransactionAdmin
)
admin.site.register(
    CSCompanyClassTuitionRecord,
    ClientSchoolCompanyClassesTuitionTransactionAdmin
)
admin.site.register(
    CSPurchasedHoursModification,
    ClientSchoolPurchasedHoursModificationRecordAdmin
)
