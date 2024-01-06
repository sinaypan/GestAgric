from django.apps import AppConfig


class gestionCentreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestionCentre'

    def ready(self):
        import gestionCentre.signals 