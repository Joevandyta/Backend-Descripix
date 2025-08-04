from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useracc'

    def ready(self):
        import useracc.signal  # Add this line to import the signals.py