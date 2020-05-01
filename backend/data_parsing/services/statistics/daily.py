from api_core.config.counties import Counties
from api_core.models import Case
from data_parsing.services.statistics.generators import generate_distribution

GROUPING_BOUNDARIES = [10, 20, 30, 40, 50, 60, 70, 80]

GLOBAL_STATISTICS = [
    {
        'field': 'county',
        'group_by_county': True,
        'search_string': 'global-county-histogram'
    },
    {
        'field': 'age',
        'grouping_boundaries': GROUPING_BOUNDARIES,
        'numeric_field': True,
        'search_string': 'global-age-histogram'
    },
    {
        'field': 'gender',
        'group_by_gender': True,
        'search_string': 'global-gender-histogram'
    },
    {
        'field': 'death_date',
        'search_string': 'global-death-date-histogram'
    }
]


def get_statistics_options_for_county(county_code):
    gender_histogram_opt = {
        'field': 'gender',
        'group_by_gender': True,
        'filters': {'county': county_code},
        'search_string': f'{county_code}-gender-histogram'
    }
    age_histogram_opt = {
        'field': 'age',
        'numeric_field': True,
        'grouping_boundaries': GROUPING_BOUNDARIES,
        'filters': {'county': county_code},
        'search_string': f'{county_code}-age-histogram'
    }
    death_date_histogram_opt = {
        'field': 'death_date',
        'filters': {'county': county_code},
        'search_string': f'{county_code}-death-date-histogram'
    }
    return gender_histogram_opt, age_histogram_opt, death_date_histogram_opt


def generate_daily_statistics():
    queryset = Case.objects.all()
    for options in GLOBAL_STATISTICS:
        generate_distribution(queryset, options)

    for county_code, _ in Counties.CHOICES:
        for options in get_statistics_options_for_county(county_code):
            generate_distribution(queryset, options)
