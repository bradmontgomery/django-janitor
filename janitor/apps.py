from django.apps import AppConfig


class JanitorConfig(AppConfig):
    name = 'janitor'

    def ready(self):
        from .models import register_everything
        register_everything()
