from datetime import datetime, timedelta
import decimal

from accounting.models import PurchasedHoursModificationRecord
from client_school_accounting.models import (
    ClientSchoolClassEnrollmentHandler,
)
from client_school_transactions.models import CSPurchasedHoursModification
from client_school_group_attendance.utils import handle_creation_of_group_class_enrollment_records


def determine_transaction_type(previous_class_status, updated_class_status):
    if previous_class_status == "scheduled" and updated_class_status == "completed":
        return "deduct"
    elif previous_class_status == "scheduled" and updated_class_status == "same_day_cancellation":
        return "deduct"
    elif previous_class_status == "cancelled" and updated_class_status == "completed":
        return "deduct"
    elif previous_class_status == "cancelled" and updated_class_status == "same_day_cancellation":
        return "deduct"
    elif previous_class_status == "completed" and updated_class_status == "scheduled":
        return "add-back"
    elif previous_class_status == "completed" and updated_class_status == "cancelled":
        return "add-back"
    elif previous_class_status == "same_day_cancellation" and updated_class_status == "scheduled":
        return "add-back"
    elif previous_class_status == "same_day_cancellation" and updated_class_status == "cancelled":
        return "add-back"
    else:
        return "unchanged"


def add_minute_to_datetime_obj(datetime_obj):
    # Create a dummy date to combine with the time
    dummy_date = datetime(1, 1, 1)

    # Combine the dummy date with the given time
    dt = datetime.combine(dummy_date, datetime_obj)

    # Add one minute
    dt_plus_1min = dt + timedelta(minutes=1)

    # Extract and return the new time
    return dt_plus_1min.time()


def time_to_hours(td, decimals=2):
    # Convert timedelta to hours
    hours = td.total_seconds() / 3600
    return round(hours, decimals)


def is_freelance_account(student_or_class):
    return student_or_class.account_type == "freelance"


def number_of_hours_purchased_should_be_updated(transaction_type):
    return transaction_type != "unchanged"


def adjust_number_of_hours_purchased(
        transaction_type, duration, previous_number_of_hours_purchased
):
    if transaction_type == "deduct":
        return previous_number_of_hours_purchased - decimal.Decimal(str(duration))
    elif transaction_type == "add-back":
        return previous_number_of_hours_purchased + decimal.Decimal(str(duration))


def determine_duration_of_class_time(start_time, finish_time):
    # calibrate time by adding one minute to the finish time
    calibrated_finish_time = add_minute_to_datetime_obj(datetime_obj=finish_time)
    # Convert time objects to timedelta, using only hours and minutes
    delta1 = timedelta(
        hours=start_time.hour, minutes=start_time.minute
    )
    delta2 = timedelta(
        hours=calibrated_finish_time.hour,
        minutes=calibrated_finish_time.minute
    )

    # Calculate the difference and return in number of hours to 2nd decimal point
    return time_to_hours(abs(delta1 - delta2))


def get_double_booked_by_user(obj_id, queried_user, student_or_teacher,
                              concurrent_booked_classes):
    if student_or_teacher == 'teacher':
        if obj_id:
            user_unavailable = [
                obj.teacher for obj in concurrent_booked_classes
                if obj.teacher == queried_user and obj.id != obj_id
            ]
        else:
            user_unavailable = [
                obj.teacher for obj in concurrent_booked_classes
                if obj.teacher == queried_user
            ]
    elif student_or_teacher == 'student':
        if obj_id:
            user_unavailable = [
                obj.student_or_class for obj in concurrent_booked_classes
                if obj.student_or_class == queried_user and obj.id != obj_id
            ]
        else:
            user_unavailable = [
                obj.student_or_class for obj in concurrent_booked_classes
                if obj.student_or_class == queried_user
            ]
    else:
        user_unavailable = []
    return user_unavailable


def class_is_double_booked(
        classes_booked_on_date, starting_time, finishing_time
):
    class_starts_during_time_frame = [
        scheduled_class for scheduled_class in classes_booked_on_date
        if starting_time <= scheduled_class.start_time <= finishing_time
    ]

    class_finishes_during_time_frame = [
        scheduled_class for scheduled_class in classes_booked_on_date
        if starting_time <= scheduled_class.finish_time <= finishing_time
    ]

    time_frame_occurs_during_a_booked_class = [
        scheduled_class for scheduled_class in classes_booked_on_date
        if starting_time >= scheduled_class.start_time
        and finishing_time <= scheduled_class.finish_time
    ]

    classes_during_date_and_time = [
        scheduled_class for scheduled_class in classes_booked_on_date
        if scheduled_class in class_starts_during_time_frame or
        scheduled_class in class_finishes_during_time_frame or
        scheduled_class in time_frame_occurs_during_a_booked_class
    ]

    return len(classes_during_date_and_time) > 0


def create_purchased_hours_modification_record(
        student_or_class, transaction_type, scheduled_class,
        previous_number_of_purchased_hours, new_number_of_purchased_hours
    ):
    if transaction_type == "add-back":
        modification_type = "class_status_modification_add"
    else: modification_type = "class_status_modification_deduct"
    PurchasedHoursModificationRecord.objects.create(
        student_or_class=student_or_class,
        modified_scheduled_class=scheduled_class,
        modification_type=modification_type,
        previous_purchased_class_hours=previous_number_of_purchased_hours,
        updated_purchased_class_hours=new_number_of_purchased_hours
    )


def handle_freelance_student_purchased_hours_modification(
        scheduled_class, student_or_class, transaction_type
    ):
        #print("******Account must be adjusted*******")
        duration = determine_duration_of_class_time(
            scheduled_class.start_time, scheduled_class.finish_time
        )
        previous_number_of_purchased_hours = student_or_class.purchased_class_hours
            
        new_number_of_purchased_hours = adjust_number_of_hours_purchased(
            transaction_type, duration, student_or_class.purchased_class_hours
        )
            
        student_or_class.purchased_class_hours = new_number_of_purchased_hours
        student_or_class.save()
            
        create_purchased_hours_modification_record(
            student_or_class=student_or_class,
            transaction_type=transaction_type,
            scheduled_class=scheduled_class,
            previous_number_of_purchased_hours=previous_number_of_purchased_hours,
            new_number_of_purchased_hours=new_number_of_purchased_hours
        )
        return {
            "id": student_or_class.id,
            "changes": {
                "purchased_class_hours": float(student_or_class.purchased_class_hours)
            }
        }


def get_client_school_enrollment_handler(student_or_class):
    try:
        return student_or_class.teachers_student_or_class_record
    except ClientSchoolClassEnrollmentHandler.DoesNotExist:
        return None


def is_client_school_account(student_or_class):
    return (
        hasattr(student_or_class, 'teachers_student_or_class_record')
        and student_or_class.teachers_student_or_class_record is not None
    )


def create_client_school_purchased_hours_modification_record(
    student_account, enrollment_handler, class_type,
    transaction_type, previous_hours, updated_hours
):
    if transaction_type == 'deduct':
        modification_type = 'class_status_modification_deduct'
    else:
        modification_type = 'class_status_modification_add'
    CSPurchasedHoursModification.objects.create(
        student_account=student_account,
        bridge=enrollment_handler,
        class_type=class_type,
        modification_type=modification_type,
        previous_hours=previous_hours,
        updated_hours=updated_hours,
    )


def format_transaction_type(transaction_type):
    if '-' in transaction_type:
        parts = transaction_type.split('-')
        return f"{parts[0]}ed-{parts[1]}"
    else:
        return f"{transaction_type}ed"


def handle_one_to_one_tutoring_hours_modification(
    enrollment_handler, transaction_type, duration
):
    student_account = enrollment_handler.client_school_one_to_one_account
    if student_account is None:
        return None
    previous_hours = student_account.purchased_tutoring_hours
    if previous_hours is None:
        return None
    duration_as_decimal = decimal.Decimal(str(duration))
    if transaction_type == 'deduct':
        updated_hours = previous_hours - duration_as_decimal
    else:
        updated_hours = previous_hours + duration_as_decimal
    student_account.purchased_tutoring_hours = updated_hours
    student_account.save()
    create_client_school_purchased_hours_modification_record(
        student_account=student_account,
        enrollment_handler=enrollment_handler,
        class_type='one_to_one_tutoring',
        transaction_type=transaction_type,
        previous_hours=previous_hours,
        updated_hours=updated_hours,
    )
    return f"Client school tutoring hours {format_transaction_type(transaction_type)}"


def handle_two_to_one_tutoring_hours_modification(
    enrollment_handler, transaction_type, duration
):
    student_accounts = enrollment_handler.client_school_two_to_one_accounts.all()
    if not student_accounts.exists():
        return None

    duration_as_decimal = decimal.Decimal(str(duration))
    updated_accounts = []

    for student_account in student_accounts:
        previous_hours = student_account.purchased_tutoring_hours
        if previous_hours is None:
            continue
        if transaction_type == 'deduct':
            updated_hours = previous_hours - duration_as_decimal
        else:
            updated_hours = previous_hours + duration_as_decimal
        student_account.purchased_tutoring_hours = updated_hours
        student_account.save()
        create_client_school_purchased_hours_modification_record(
            student_account=student_account,
            enrollment_handler=enrollment_handler,
            class_type='two_to_one_tutoring',
            transaction_type=transaction_type,
            previous_hours=previous_hours,
            updated_hours=updated_hours,
        )
        updated_accounts.append(student_account.client_student_name)

    if not updated_accounts:
        return None

    return f"Client school two-to-one tutoring hours {format_transaction_type(transaction_type)}"


def handle_online_tutoring_hours_modification(
    enrollment_handler, transaction_type, duration
):
    student_account = enrollment_handler.client_school_online_account
    if student_account is None:
        return None
    previous_hours = student_account.purchased_online_hours
    if previous_hours is None:
        return None
    duration_as_decimal = decimal.Decimal(str(duration))
    if transaction_type == 'deduct':
        updated_hours = previous_hours - duration_as_decimal
    else:
        updated_hours = previous_hours + duration_as_decimal
    student_account.purchased_online_hours = updated_hours
    student_account.save()
    create_client_school_purchased_hours_modification_record(
        student_account=student_account,
        enrollment_handler=enrollment_handler,
        class_type='online_tutoring',
        transaction_type=transaction_type,
        previous_hours=previous_hours,
        updated_hours=updated_hours,
    )
    return f"Client school online tutoring hours {format_transaction_type(transaction_type)}"


def handle_company_class_hours_modification(
    enrollment_handler, transaction_type, duration
):
    student_account = enrollment_handler.client_school_company_account
    if student_account is None:
        return None
    previous_hours = student_account.purchased_company_hours
    if previous_hours is None:
        return None
    duration_as_decimal = decimal.Decimal(str(duration))
    if transaction_type == 'deduct':
        updated_hours = previous_hours - duration_as_decimal
    else:
        updated_hours = previous_hours + duration_as_decimal
    student_account.purchased_company_hours = updated_hours
    student_account.save()
    create_client_school_purchased_hours_modification_record(
        student_account=student_account,
        enrollment_handler=enrollment_handler,
        class_type='company_class',
        transaction_type=transaction_type,
        previous_hours=previous_hours,
        updated_hours=updated_hours,
    )
    return f"Client company class tutoring hours {format_transaction_type(transaction_type)}"


def handle_client_school_purchased_hours_modification(
    scheduled_class, student_or_class, transaction_type
):
    enrollment_handler = get_client_school_enrollment_handler(student_or_class)
    if enrollment_handler is None:
        return None

    duration = determine_duration_of_class_time(
        scheduled_class.start_time, scheduled_class.finish_time
    )
    class_enrollment_type = enrollment_handler.class_enrollment_type

    if class_enrollment_type == 'one_to_one_tutoring':
        return {
            'message': handle_one_to_one_tutoring_hours_modification(
                enrollment_handler, transaction_type, duration
            ),
            'meeting_record_id': None,
        }
    elif class_enrollment_type == 'two_to_one_tutoring':
        return {
            'message': handle_two_to_one_tutoring_hours_modification(
                enrollment_handler, transaction_type, duration
            ),
            'meeting_record_id': None,
        }
    elif class_enrollment_type == 'online_tutoring':
        return {
            'message': handle_online_tutoring_hours_modification(
                enrollment_handler, transaction_type, duration
            ),
            'meeting_record_id': None,
        }
    elif class_enrollment_type == 'company_class':
        return {
            'message': handle_company_class_hours_modification(
                enrollment_handler, transaction_type, duration
            ),
            'meeting_record_id': None,
        }
    elif class_enrollment_type == 'group_class':
        if transaction_type == 'deduct':
            return handle_creation_of_group_class_enrollment_records(
                scheduled_class=scheduled_class,
                enrollment_handler=enrollment_handler,
                duration=duration,
            )
        else:
            return {
                'message': 'Group class status changed — no attendance records created',
                'meeting_record_id': None,
            }

    return None
