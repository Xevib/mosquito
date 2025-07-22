from django.apps import AppConfig


class MosquitoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.mosquito_app'

    def ready(self):
        import src.mosquito_app.signals