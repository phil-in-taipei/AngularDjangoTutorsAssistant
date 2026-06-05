from django.apps import AppConfig


class ClientSchoolGroupAttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_school_group_attendance'

    def ready(self):
        import client_school_group_attendance.staff_admin  # triggers the registration
