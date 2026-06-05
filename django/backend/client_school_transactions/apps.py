from django.apps import AppConfig


class ClientSchoolTransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_school_transactions'

    def ready(self):
        import client_school_transactions.staff_admin  # triggers the registration
