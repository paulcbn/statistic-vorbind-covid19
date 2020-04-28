import ast

from django.apps import apps
from django.core.management import BaseCommand

from api_core.models import Case
from data_parsing.services.statistics.generators import generate_distribution


class Command(BaseCommand):
    help = 'Generates statistics based on a specified model. See README.MD for manual'

    DISTRIBUTION_ALIAS = ['distribution', 'distr', 'dist', 'd']
    HISTOGRAM_ALIAS = ['histogram', 'hist', 'h']

    def add_arguments(self, parser):
        # parser.add_argument('app', action='store', type=str, help="App name", default="api_core")
        # parser.add_argument('model', action='store', type=str, help="Model name", default="Case")
        # parser.add_argument('--type', help='Statistics type (currently not used, more probably in the future)',
        #                     default=self.DISTRIBUTION_ALIAS[0])
        parser.add_argument('--filters', type=ast.literal_eval, help="(Optional) Filters dataset before processing",
                            default={})
        parser.add_argument('--fields', nargs='+', type=str, help="Fields of model")
        parser.add_argument('--group', nargs='+', type=int, default=[])
        parser.add_argument('--group_by_gender', type=bool, default=False)
        parser.add_argument('--group_by_county', type=bool, default=False)

    def handle(self, *args, **options):
        stats_type = options.get("type")
        # model = apps.get_app_config(options.get('app')).get_model(model_name=options.get('model'))
        model = Case
        qs = model.objects.filter(**options.get('filters'))
        # if stats_type in self.DISTRIBUTION_ALIAS:
        return generate_distribution(qs, options)
        # raise ValueError("Invalid statistics type '{}'".format(stats_type))
