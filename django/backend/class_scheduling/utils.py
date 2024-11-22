from datetime import datetime, timedelta
import decimal


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
        return "refund"
    elif previous_class_status == "completed" and updated_class_status == "cancelled":
        return "refund"
    elif previous_class_status == "same_day_cancellation" and updated_class_status == "scheduled":
        return "refund"
    elif previous_class_status == "same_day_cancellation" and updated_class_status == "cancelled":
        return "refund"
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
    return transaction_type is not "unchanged"


def adjust_number_of_hours_purchased(
        transaction_type, duration, previous_number_of_hours_purchased
):
    if transaction_type == "deduct":
        return previous_number_of_hours_purchased - decimal.Decimal(str(duration))
    elif transaction_type == "refund":
        return previous_number_of_hours_purchased + decimal.Decimal(str(duration))


def determine_duration_of_class_time(start_time, finish_time):
    print(start_time)
    print(finish_time)
    # calibrate time by adding one minute to the finish time
    calibrated_finish_time = add_minute_to_datetime_obj(datetime_obj=finish_time)
    print(calibrated_finish_time)
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
    print(classes_during_date_and_time)

    return len(classes_during_date_and_time) > 0
