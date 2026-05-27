from decimal import Decimal

from client_school_group_attendance.models import (
    GroupClassMeetingRecord,
    GroupClassStudentAttendanceRecord,
)
from client_school_transactions.models import CSPurchasedHoursModification



def handle_creation_of_group_class_enrollment_records(
    scheduled_class, enrollment_handler, duration
):
    group_class = enrollment_handler.client_group_class
    if group_class is None:
        return None

    teacher = scheduled_class.teacher
    teacher_name = f"{teacher.given_name} {teacher.surname}"

    meeting_record = GroupClassMeetingRecord.objects.create(
        scheduled_class=scheduled_class,
        group_class=group_class,
        teacher_name=teacher_name,
        class_date=scheduled_class.date,
        class_duration=duration,
    )

    enrolled_students = group_class.client_group_class_accounts.all()
    for student_account in enrolled_students:
        GroupClassStudentAttendanceRecord.objects.create(
            group_class_meeting_record=meeting_record,
            student_account=student_account,
            attendance_status='scheduled',
        )

    return f"Group class meeting record created for {group_class.group_class_name} with {enrolled_students.count()} students"


def create_group_class_purchased_hours_modification_record(
    student_account, attendance_record, transaction_type,
    previous_hours, updated_hours
):
    if transaction_type == 'deduct':
        modification_type = 'class_status_modification_deduct'
    else:
        modification_type = 'class_status_modification_add'
    meeting_record = attendance_record.group_class_meeting_record
    enrollment_handler = meeting_record.group_class.group_class_account_enrollment.filter(
        student_or_class__isnull=False
    ).first()
    CSPurchasedHoursModification.objects.create(
        student_account=student_account,
        bridge=enrollment_handler,
        class_type='group_class',
        modification_type=modification_type,
        previous_hours=previous_hours,
        updated_hours=updated_hours,
    )


def handle_group_class_attendance_hours_modification(
    attendance_record, previous_status
):
    from class_scheduling.utils import determine_transaction_type
    updated_status = attendance_record.attendance_status
    transaction_type = determine_transaction_type(
        previous_class_status=previous_status,
        updated_class_status=updated_status,
    )

    if transaction_type == 'unchanged':
        return None

    student_account = attendance_record.student_account
    if student_account.purchased_group_class_hours is None:
        return None

    meeting_record = attendance_record.group_class_meeting_record
    duration_as_decimal = Decimal(str(meeting_record.class_duration))
    previous_hours = student_account.purchased_group_class_hours

    if transaction_type == 'deduct':
        updated_hours = previous_hours - duration_as_decimal
    else:
        updated_hours = previous_hours + duration_as_decimal

    student_account.purchased_group_class_hours = updated_hours
    student_account.save()

    create_group_class_purchased_hours_modification_record(
        student_account=student_account,
        attendance_record=attendance_record,
        transaction_type=transaction_type,
        previous_hours=previous_hours,
        updated_hours=updated_hours,
    )

    return (
        f"Group class hours {transaction_type}ed for "
        f"{student_account.client_student_name}: "
        f"{previous_hours} → {updated_hours}"
    )
