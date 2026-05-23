from django.utils import timezone
from class_scheduling.models import ScheduledClass
from client_school_accounting.models import AccountingClientSchoolGroupClass
from client_school_group_attendance.models import (
    GroupClassMeetingRecord,
    GroupClassStudentAttendanceRecord,
)


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
