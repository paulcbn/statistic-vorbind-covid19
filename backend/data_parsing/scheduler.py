import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import register_events

from data_parsing.tasks import process_data_task

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(process_data_task, "cron", id="Process data", hour="*/3", minute="0", replace_existing=True)
    logging.debug("Import data successfully!")
    register_events(scheduler)

    scheduler.start()
