from django.core.management import BaseCommand

from data_parsing.services.statistics.daily import generate_daily_statistics


class Command(BaseCommand):
    help = 'Generate daily statistics'

    def handle(self, *args, **options):
        generate_daily_statistics()
