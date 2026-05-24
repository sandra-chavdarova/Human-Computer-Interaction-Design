from django.apps import AppConfig


class EstatesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estates_app'

    def ready(self):
        import estates_app.signals
