from calendar import monthrange
from datetime import datetime, timedelta

from class_scheduling.models import ScheduledClass
from venues.utils import get_available_spaces_at_venue


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
            teacher=recurring_class.teacher,
            location=recurring_class.recurring_location
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
        #print(date)
        if ScheduledClass.custom_query.teacher_already_booked_classes_during_date_and_time(
            query_date=date, 
            starting_time=recurring_class.recurring_start_time, 
            finishing_time=recurring_class.recurring_finish_time, 
            teacher_id=recurring_class.teacher
        ):
            return True
    return False


def recurring_class_applied_monthly_has_double_booked_location(
        list_of_dates_on_day_in_given_month,
        recurring_class
):
    for date in list_of_dates_on_day_in_given_month:
        #print(date)
        if ScheduledClass.custom_query.location_already_booked_during_date_and_time(
            query_date=date,
            starting_time=recurring_class.recurring_start_time,
            finishing_time=recurring_class.recurring_finish_time,
            location_id=recurring_class.recurring_location
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
    #print(classes_during_day_of_week_and_time)

    return len(classes_during_day_of_week_and_time) > 0


def get_list_of_double_booked_recurring_classes(
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
    #print(classes_during_day_of_week_and_time)

    return classes_during_day_of_week_and_time


def get_double_booked_recurring_classes_data(
    recurring_classes_booked_on_day_of_week, recurring_start_time, recurring_finish_time
):
    double_booked_classes = get_list_of_double_booked_recurring_classes(
        recurring_classes_booked_on_day_of_week,
        recurring_start_time,
        recurring_finish_time,
    )
    return {
        "class_is_double_booked": len(double_booked_classes) > 0,
        "double_booked_classes": double_booked_classes,
    }


def create_teacher_recurring_double_booking_error_message(
    day_of_week, double_booked_classes
):
    """
    Build an error message for a teacher who has been double booked
    on a recurring day of the week.

    Args:
        day_of_week: string.
        double_booked_classes: a list of RecurringScheduledClass objects
            that clash.

    Returns:
        1 item:   "Teacher double booked Anna (09:00-10:00) on Monday"
        2 items:  "Teacher double booked Anna (09:00-10:00) and Ben (09:30-10:30) on Monday"
        3+ items: "Teacher double booked Anna (09:00-10:00), Ben (09:30-10:30), and Class C (10:00-11:00) on Monday"
    """
    def format_time(time_value):
        return time_value.strftime("%H:%M") if time_value else "??:??"

    def describe(recurring_class):
        return "{} ({}-{})".format(
            recurring_class.student_or_class.student_or_class_name,
            format_time(recurring_class.recurring_start_time),
            format_time(recurring_class.recurring_finish_time),
        )

    descriptions = [describe(rc) for rc in double_booked_classes]

    if not descriptions:
        raise ValueError("double_booked_classes must contain at least one item.")

    if len(descriptions) == 1:
        classes_text = descriptions[0]
    elif len(descriptions) == 2:
        classes_text = "{} and {}".format(*descriptions)
    else:
        classes_text = "{}, and {}".format(
            ", ".join(descriptions[:-1]), descriptions[-1]
        )

    return "Double booking: {} on {}".format(
        classes_text, day_of_week
    )


def get_list_of_recurring_locations_from_list_of_recurring_classes(list_of_recurring_classes):
    return [rc.recurring_location for rc in list_of_recurring_classes]


def get_double_booked_recurring_classes_location_data(
    recurring_classes_booked_on_day_of_week,
    recurring_start_time, recurring_finish_time,
    recurring_location
):
    potential_double_booked_classes = get_list_of_double_booked_recurring_classes(
        recurring_classes_booked_on_day_of_week,
        recurring_start_time,
        recurring_finish_time,
    )
    locations_booked_during_recurring_time = get_list_of_recurring_locations_from_list_of_recurring_classes(
        list_of_recurring_classes=potential_double_booked_classes
    )
    return {
        "class_is_double_booked": recurring_location in locations_booked_during_recurring_time,
        "booked_locations_at_venue": locations_booked_during_recurring_time,
    }


def create_venue_space_recurring_double_booking_error_message(venue, booked_spaces):
    """
    Build an error message for a teacher who has tried to schedule a class
    in a venue space that is already booked.

    Args:
        venue: a Venue instance.
        booked_spaces: an iterable of VenueSpace instances (or a QuerySet)
            that are already booked at the venue for the time period.

    Returns:
        0 available: "Venue space already booked at Cafe Luna. No other spaces are available during that time."
        1 available: "Venue space already booked at Cafe Luna. Available space: Table 1"
        2 available: "Venue space already booked at Cafe Luna. Available spaces: Table 1 and Table 2"
        3+ available: "Venue space already booked at Cafe Luna. Available spaces: Table 1, Table 2, and Table 3"
    """
    available_spaces = get_available_spaces_at_venue(venue, booked_spaces)
    names = [space.space_name for space in available_spaces]

    base_message = "Space already booked at {}.".format(venue.venue_name)

    if not names:
        return "{} No other spaces are available during that time.".format(
            base_message
        )

    if len(names) == 1:
        spaces_text = names[0]
        label = "Available space"
    elif len(names) == 2:
        spaces_text = "{} and {}".format(*names)
        label = "Available spaces"
    else:
        spaces_text = "{}, and {}".format(", ".join(names[:-1]), names[-1])
        label = "Available spaces"

    return "{} {}: {}".format(base_message, label, spaces_text)
