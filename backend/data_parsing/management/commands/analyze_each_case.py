from django.core.management.base import BaseCommand

from data_parsing.services.case_analyzer.case_analyzer_service import analyze_all_cases


class Command(BaseCommand):
    help = 'Analizeaza fiecare caz in parte pe baza surselor de date colectate. '

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite all fields that already have a value instead of ignoring them.'
        )

    def handle(self, *args, **options):
        overwrite = options.get('overwrite', False)
        analyze_all_cases(force_overwrite=overwrite)
