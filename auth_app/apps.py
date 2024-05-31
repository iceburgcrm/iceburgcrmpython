from django.apps import AppConfig
from .orator_config import setup_orator

class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        setup_orator()  

