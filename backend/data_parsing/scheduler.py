import logging

from django.conf import settings
from django_apscheduler.jobstores import register_events

from data_parsing.scheduler_instance import SchedulerSingleton
from data_parsing.tasks import process_data_task

scheduler = SchedulerSingleton.get_instance()


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(process_data_task, "cron", id="Process data", hour="*/1", minute="0", replace_existing=True)
    logging.info("Job started successfully!")
    register_events(scheduler)

    scheduler.start()
