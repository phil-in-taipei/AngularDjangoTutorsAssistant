from django.apps import AppConfig


class RecurringSchedulingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recurring_scheduling'

    def ready(self):
        import recurring_scheduling.staff_admin
