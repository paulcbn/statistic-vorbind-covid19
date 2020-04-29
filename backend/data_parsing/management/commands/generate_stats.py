import ast

from django.core.management import BaseCommand

from api_core.models import Case
from data_parsing.services.statistics.generators import generate_distribution


class Command(BaseCommand):
    help = 'Generates statistics based on a specified model. See README.MD for manual'

    DISTRIBUTION_ALIAS = ['distribution', 'distr', 'dist', 'd']
    HISTOGRAM_ALIAS = ['histogram', 'hist', 'h']

    def add_arguments(self, parser):
        parser.add_argument('--filters', type=ast.literal_eval, help="(Optional) Filters dataset before processing",
                            default={})
        parser.add_argument('--field', type=str, help="Field of the model")
        parser.add_argument('--grouping_boundaries', nargs='+', type=int, default=[])
        parser.add_argument('--group_by_gender', action='store_true', default=False)
        parser.add_argument('--group_by_county', action='store_true', default=False)
        parser.add_argument('--search_string', default=None)

    def handle(self, *args, **options):
        qs = Case.objects.filter(**options.get('filters'))
        return generate_distribution(qs, options)
