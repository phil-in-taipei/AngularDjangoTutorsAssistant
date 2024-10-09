import datetime


def determine_transaction_type(previous_class_status, updated_class_status):
    if previous_class_status == "scheduled" and updated_class_status == "completed":
        return "deduct"
    elif previous_class_status == "scheduled" and updated_class_status == "same_day_cancellation":
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


def determine_duration_of_class_time(start_time, finish_time):
    print(start_time)
    print(finish_time)



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
