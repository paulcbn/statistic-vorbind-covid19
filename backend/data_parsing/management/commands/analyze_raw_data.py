from django.core.management.base import BaseCommand


from data_parsing.services.raw_data_analyzer_service import create_deaths_from_data_sources


class Command(BaseCommand):
    help = 'Analizeaza sursele de date'

    def handle(self, *args, **options):
        create_deaths_from_data_sources()
