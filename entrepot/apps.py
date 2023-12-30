from django.apps import AppConfig


class EntrepotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entrepot'

    def ready(self):
        import entrepot.signals 