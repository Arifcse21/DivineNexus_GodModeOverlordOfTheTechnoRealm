from django.apps import AppConfig
from django.db.models.signals import post_migrate



class TechnoDominantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'techno_dominant'

    def ready(self) -> None:
        from techno_dominant.utils.model_utils import create_weekdays
        post_migrate.connect(create_weekdays, sender=self)


    
