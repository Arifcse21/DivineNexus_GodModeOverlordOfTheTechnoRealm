from django.apps import AppConfig
from django.db.models.signals import post_migrate



class TechnoDominantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'techno_dominant'

    def ready(self):
        from techno_dominant.models import DominantCliModel
        from techno_dominant.signals.dominant_signals import dominant_cli_signal
        post_migrate.connect(dominant_cli_signal, sender=DominantCliModel)
    
