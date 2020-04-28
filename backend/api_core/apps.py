from django.apps import AppConfig
from django.conf import settings


class ApiCoreConfig(AppConfig):
    name = 'api_core'

    def ready(self):
        from backend.data_parsing import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
