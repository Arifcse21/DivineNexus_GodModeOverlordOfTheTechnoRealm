from django.apps import AppConfig


class TechnoDominantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'techno_dominant'

    # def ready(self) -> None:
    #     from techno_dominant import signals
    
