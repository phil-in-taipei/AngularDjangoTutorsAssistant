from calendar import monthrange
from datetime import datetime, timedelta

from class_scheduling.models import ScheduledClass


def create_date_list(year, month, day_of_week):
    delta = timedelta(days=1)
    start = datetime(year, month, 1)
    finish = datetime(year, month, (monthrange(year, month)[1]))
    list_of_dates_on_day_in_given_month = []
    while start <= finish:
        if start.weekday() == day_of_week:
            list_of_dates_on_day_in_given_month.append(start.date())
        start += delta
    #print('These are the dates for that period:')
    #print(list_of_dates_on_day_in_given_month)
    return list_of_dates_on_day_in_given_month


def book_classes_for_specified_month(date_list, recurring_class):
    for date in date_list:
        #print('booking new classes:')
        new_booking_obj, created = ScheduledClass.objects.get_or_create(
            date=date,
            start_time=recurring_class.recurring_start_time,
            finish_time=recurring_class.recurring_finish_time,
            student_or_class=recurring_class.student_or_class,
            teacher=recurring_class.teacher
            )
        #print(new_booking_obj)
        #print(created)
        if created:
            new_booking_obj.save()


def get_classes_for_deletion_for_specified_month(date_list, recurring_class):
    objs_for_deletion = []
    for date in date_list:
        booking_obj_for_deletion = ScheduledClass.objects.filter(
            date=date,
            start_time=recurring_class.recurring_start_time,
            finish_time=recurring_class.recurring_finish_time,
            student_or_class=recurring_class.student_or_class,
            teacher=recurring_class.teacher
        ).first()
        #print(booking_obj_for_deletion)
        if booking_obj_for_deletion:
            objs_for_deletion.append(booking_obj_for_deletion)
    return objs_for_deletion


def recurring_class_applied_monthly_has_scheduling_conflict(
        list_of_dates_on_day_in_given_month,
        recurring_class
):
    for date in list_of_dates_on_day_in_given_month:
        print(date)
        if ScheduledClass.custom_query.teacher_already_booked_classes_during_date_and_time(
            query_date=date, 
            starting_time=recurring_class.recurring_start_time, 
            finishing_time=recurring_class.recurring_finish_time, 
            teacher_id=recurring_class.teacher
        ):
            return True
    return False

def recurring_class_is_double_booked(
        recurring_classes_booked_on_day_of_week, recurring_start_time, recurring_finish_time
):
    class_starts_during_time_frame = [
        recurring_class for recurring_class in recurring_classes_booked_on_day_of_week
        if recurring_start_time <= recurring_class.recurring_start_time <= recurring_finish_time
    ]

    class_finishes_during_time_frame = [
        recurring_class for recurring_class in recurring_classes_booked_on_day_of_week
        if recurring_start_time <= recurring_class.recurring_finish_time <= recurring_finish_time
    ]

    time_frame_occurs_during_a_booked_class = [
        recurring_class for recurring_class in recurring_classes_booked_on_day_of_week
        if recurring_start_time >= recurring_class.recurring_start_time
        and recurring_finish_time <= recurring_class.recurring_finish_time
    ]

    classes_during_day_of_week_and_time = [
        recurring_class for recurring_class in recurring_classes_booked_on_day_of_week
        if recurring_class in class_starts_during_time_frame or
        recurring_class in class_finishes_during_time_frame or
        recurring_class in time_frame_occurs_during_a_booked_class
    ]
    print(classes_during_day_of_week_and_time)

    return len(classes_during_day_of_week_and_time) > 0
