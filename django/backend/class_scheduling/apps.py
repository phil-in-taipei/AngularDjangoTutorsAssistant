from django.apps import AppConfig


class ClassSchedulingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'class_scheduling'

    def ready(self):
        import class_scheduling.staff_admin  # triggers the registration
