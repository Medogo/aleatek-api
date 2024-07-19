from django.apps import AppConfig


class DashbordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dashbord'

    def ready(self):
        import Dashbord.signals  