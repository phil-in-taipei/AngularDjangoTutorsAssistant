

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
