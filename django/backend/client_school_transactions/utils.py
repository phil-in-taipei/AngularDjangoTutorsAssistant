from .models import (
    ClientSchoolPurchasedHoursModificationRecord,
)
from client_school_accounting.models import AccountingClientSchoolStudentAccount


def create_modification_record_for_tutoring_transaction(
    previous_hours_purchased, tutoring_transaction
):
    if tutoring_transaction.transaction_type == 'payment':
        modification_type = 'tuition_payment_add'
    else:
        modification_type = 'tuition_refund_deduct'
    student_account = AccountingClientSchoolStudentAccount.objects.get(
        id=tutoring_transaction.student_account.id
    )
    ClientSchoolPurchasedHoursModificationRecord.objects.create(
        student_account=student_account,
        tutoring_transaction=tutoring_transaction,
        class_type='one_to_one_tutoring',
        modification_type=modification_type,
        previous_hours=previous_hours_purchased,
        updated_hours=student_account.purchased_tutoring_hours,
    )


def create_modification_record_for_two_to_one_transaction(
    previous_hours_purchased, two_to_one_transaction
):
    if two_to_one_transaction.transaction_type == 'payment':
        modification_type = 'tuition_payment_add'
    else:
        modification_type = 'tuition_refund_deduct'
    student_account = AccountingClientSchoolStudentAccount.objects.get(
        id=two_to_one_transaction.primary_student_account.id
    )
    ClientSchoolPurchasedHoursModificationRecord.objects.create(
        student_account=student_account,
        two_to_one_transaction=two_to_one_transaction,
        class_type='two_to_one_tutoring',
        modification_type=modification_type,
        previous_hours=previous_hours_purchased,
        updated_hours=student_account.purchased_tutoring_hours,
    )


def create_modification_record_for_online_transaction(
    previous_hours_purchased, online_transaction
):
    if online_transaction.transaction_type == 'payment':
        modification_type = 'tuition_payment_add'
    else:
        modification_type = 'tuition_refund_deduct'
    student_account = AccountingClientSchoolStudentAccount.objects.get(
        id=online_transaction.student_account.id
    )
    ClientSchoolPurchasedHoursModificationRecord.objects.create(
        student_account=student_account,
        online_transaction=online_transaction,
        class_type='online_tutoring',
        modification_type=modification_type,
        previous_hours=previous_hours_purchased,
        updated_hours=student_account.purchased_online_hours,
    )


def create_modification_record_for_group_transaction(
    previous_hours_purchased, group_transaction
):
    if group_transaction.transaction_type == 'payment':
        modification_type = 'tuition_payment_add'
    else:
        modification_type = 'tuition_refund_deduct'
    student_account = AccountingClientSchoolStudentAccount.objects.get(
        id=group_transaction.student_account.id
    )
    ClientSchoolPurchasedHoursModificationRecord.objects.create(
        student_account=student_account,
        group_transaction=group_transaction,
        class_type='group_class',
        modification_type=modification_type,
        previous_hours=previous_hours_purchased,
        updated_hours=student_account.purchased_group_class_hours,
    )


def create_modification_record_for_company_transaction(
    previous_hours_purchased, company_transaction
):
    if company_transaction.transaction_type == 'payment':
        modification_type = 'tuition_payment_add'
    else:
        modification_type = 'tuition_refund_deduct'
    student_account = AccountingClientSchoolStudentAccount.objects.get(
        id=company_transaction.student_account.id
    )
    ClientSchoolPurchasedHoursModificationRecord.objects.create(
        student_account=student_account,
        company_transaction=company_transaction,
        class_type='company_class',
        modification_type=modification_type,
        previous_hours=previous_hours_purchased,
        updated_hours=student_account.purchased_company_hours,
    )