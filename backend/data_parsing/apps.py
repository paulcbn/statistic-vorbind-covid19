from django.apps import AppConfig

from backend import settings


class DataParsingConfig(AppConfig):
    name = 'data_parsing'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
