from student_account.models import StudentOrClass
from .models import PurchasedHoursModificationRecord
 

def create_purchased_hours_modification_record_for_tuition_transaction(
        previous_hours_purchased, freelance_tuition_transaction_record,
):
    if freelance_tuition_transaction_record.tuition_transaction == "payment":
        modification_type = "tuition_payment_add"
    else:
        modification_type = "tuition_payment_deduct"
    student_or_class=StudentOrClass.objects.get(
        id=freelance_tuition_transaction_record.student_or_class.id
    )
    PurchasedHoursModificationRecord.objects.create(
        student_or_class=student_or_class,
        tuition_transaction=freelance_tuition_transaction_record,
        modification_type=modification_type,
        previous_purchased_class_hours=previous_hours_purchased,
        updated_purchased_class_hours=student_or_class.purchased_class_hours
    )

