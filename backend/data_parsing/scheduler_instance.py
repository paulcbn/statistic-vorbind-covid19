import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings


class SchedulerSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not SchedulerSingleton.__instance:
            SchedulerSingleton()
        return SchedulerSingleton.__instance

    def __init__(self):
        if SchedulerSingleton.__instance:
            logging.error("Tried to reinitialized singleton class.")
        else:
            SchedulerSingleton.__instance = BackgroundScheduler(settings.SCHEDULER_CONFIG)
