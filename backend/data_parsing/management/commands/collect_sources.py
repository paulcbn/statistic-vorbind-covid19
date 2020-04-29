from django.core.management.base import BaseCommand

from data_parsing.services.sources_collector_service import collect_data_sources


class Command(BaseCommand):
    help = 'Colecteaza sursele de date'

    def add_arguments(self, parser):
        parser.add_argument('pages', type=int)

    def handle(self, *args, **options):
        pages = options['pages']
        collect_data_sources(base_url="https://stirioficiale.ro/informatii", page_count=pages)
