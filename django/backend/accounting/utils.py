from datetime import date, datetime, timedelta
from django.db.models import Case, When, Value, IntegerField
from django.utils.timezone import make_aware, get_current_timezone

from class_scheduling.models import ScheduledClass
from student_account.models import StudentOrClass
from .models import PurchasedHoursModificationRecord
 
from pprint import pprint


def create_purchased_hours_modification_record_for_tuition_transaction(
        previous_hours_purchased, freelance_tuition_transaction_record,
):
    if freelance_tuition_transaction_record.transaction_type == "payment":
        modification_type = "tuition_payment_add"
    else:
        modification_type = "tuition_refund_deduct"
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
    print("----------------------------------------------------------------------")
    print(F"These are the previous hours purchased: {previous_hours_purchased}")
    print("----------------------------------------------------------------------")
    print(F"These are the updated hours purchased: {student_or_class.purchased_class_hours}")
    print("----------------------------------------------------------------------")


def create_timestamps_for_beginning_and_end_of_month_and_year(month: int, year: int) -> dict:
    """
    Generate timestamps for the beginning and end of a specific month and year.
    
    Args:
        month (int): The month (1-12)
        year (int): The year
    
    Returns:
        dict: A dictionary with 'start' and 'end' keys containing timestamps
    
    Note: 
    - Uses Django's make_aware to ensure timezone-aware timestamps
    - Assumes the current system timezone (can be modified if needed)
    """
    start_of_month = datetime(year, month, 1, 0, 0, 0)
    
    if month == 12:
        # For December, next month is January of the next year
        end_of_month = datetime(year, month, 31, 23, 59, 59)
    else:
        # For other months, use the day before the first day of the next month
        next_month_first_day = datetime(year, month + 1, 1)
        end_of_month = next_month_first_day - timedelta(seconds=1)
    
    # Make timestamps timezone-aware
    start_timestamp = make_aware(start_of_month, get_current_timezone())
    end_timestamp = make_aware(end_of_month, get_current_timezone())
    
    return {
        'start': start_timestamp,
        'end': end_timestamp
    }


def get_scheduled_classes_during_month_period(
        teacher, month, year
):
    start_date = date(int(year), int(month), 1)
    if int(month) == 12:
        finish_date = date(int(year) + 1, 1, 1)
    else:
        finish_date = date(int(year), int(month) + 1, 1)

    queryset = ScheduledClass.objects.filter(
                date__gte=start_date,
                date__lt=finish_date,
                teacher=teacher
        )
    return queryset.order_by(
        Case(
            When(student_or_class__school__isnull=True, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        'student_or_class__school__school_name'  # Then by school name
    )


def generate_estimated_earnings_report(
        teacher, month, year
):
    sorted_classes = get_scheduled_classes_during_month_period(
        teacher, month, year
    )
    print("************This is the query result************")
    pprint(list(sorted_classes))
    return sorted_classes

