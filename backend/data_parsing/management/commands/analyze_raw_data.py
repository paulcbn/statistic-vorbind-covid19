import datetime
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from data_parsing.services.raw_data_analyzer_service import create_deaths_from_data_sources

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Analizeaza sursele de date'
    date_format = '%Y-%m-%d'

    def add_arguments(self, parser):
        parser.add_argument(
            '--today',
            action='store_true',
            help='Analyze data that was created today.'
        )

        parser.add_argument(
            '--between',
            nargs=2,
            help='Analyze data that was created today.'
        )

    def try_parse_dates(self, dates):
        if dates is None:
            return None, None

        try:
            start = datetime.datetime.strptime(dates[0], self.date_format)
            end = datetime.datetime.strptime(dates[1], self.date_format)
            start = timezone.make_aware(start, timezone.get_current_timezone())
            end = timezone.make_aware(end, timezone.get_current_timezone())

            return start, end
        except ValueError:
            return None, None

    def handle(self, *args, **options):
        today = options.get('today', False)

        between = options.get('between', None)
        start, end = None, None
        if between is not None:
            start, end = self.try_parse_dates(options.get('between'))
            if start is None and end is None:
                logger.error(f"Invalid dates :'{start}', '{end}'.")
                return

        create_deaths_from_data_sources(today=today, start_date=start, end_date=end)
