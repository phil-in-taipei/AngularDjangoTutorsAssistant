from django.apps import AppConfig


class ClientSchoolAccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_school_accounting'

    def ready(self):
        import client_school_accounting.staff_admin  # triggers the registration
