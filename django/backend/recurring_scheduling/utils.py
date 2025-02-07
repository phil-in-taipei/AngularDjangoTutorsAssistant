
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
