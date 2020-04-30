import dataclasses
import json
import uuid
from dataclasses import dataclass
from math import sqrt

from django.db.models import Max, Avg, Count, Min, StdDev

from api_core.config.counties import Counties
from api_core.models import Statistic, Case
from data_parsing.services.statistics.json_utils import json_converter


@dataclass
class GroupedDataEntry:
    key: int
    value: int
    label: str


def get_group_index(value, boundaries):
    if value <= boundaries[0]:
        return 0
    for j in range(0, len(boundaries) - 1):
        if boundaries[j] < value <= boundaries[j + 1]:
            return j + 1
    return len(boundaries)


def create_groups(boundaries):
    groups = []
    boundaries_count = len(boundaries)
    for index in range(boundaries_count - 1):
        lower_bound = boundaries[index]
        upper_bound = boundaries[index + 1] - 1
        key = index + 1
        groups.append((lower_bound, upper_bound, key))

    if len(boundaries) > 0:
        groups = [(None, boundaries[0] - 1, 0)] + groups + [(boundaries[-1], None, boundaries_count + 1)]

    return groups


def create_bounding_filter(field, lower_bound, upper_bound):
    filter_dict = dict()
    if lower_bound:
        filter_dict[f'{field}__gte'] = lower_bound
    if upper_bound:
        filter_dict[f'{field}__lte'] = upper_bound
    return filter_dict


def create_bounding_label(lower_bound, upper_bound):
    if lower_bound and upper_bound:
        return f'{lower_bound} - {upper_bound}'

    if lower_bound:
        return f'după {lower_bound}'

    if upper_bound:
        return f'până în {upper_bound}'

    return '-'


def get_distribution_by_boundary_grouping(queryset, field, grouping_boundaries):
    groups = create_groups(grouping_boundaries)
    data = []
    for lower_bound, upper_bound, key in groups:
        filter_dict = create_bounding_filter(field, lower_bound, upper_bound)
        label = create_bounding_label(lower_bound, upper_bound)
        value = queryset.filter(**filter_dict).count()

        data.append(GroupedDataEntry(value=value, label=label, key=key))

    return data


def get_distribution_by_gender_grouping(queryset, field):
    data = []
    for key, gender in enumerate((Case.MALE, Case.FEMALE)):
        value = queryset.filter(gender=gender).aggregate(count=Count(field)).get('count')
        data.append(GroupedDataEntry(value=value, label=gender, key=key))
    return data


def get_distribution_by_county_grouping(queryset, field):
    data = []
    for key, county in enumerate(Counties.CHOICES):
        county_code, _ = county
        value = queryset.filter(county=county_code).aggregate(count=Count(field)).get('count')
        data.append(GroupedDataEntry(value=value, label=county_code, key=key))
    return data


def get_distribution(queryset, field):
    result = []
    for key, tuple_ in enumerate(queryset.values(field).annotate(count=Count(field)).order_by(field).values_list(field,
                                                                                                                 'count')):
        field_value, count_value = tuple_
        result.append(GroupedDataEntry(key=key, value=count_value, label=field_value))
    return result


def get_serializable_data(data):
    dict_list = map(dataclasses.asdict, data)
    return list(dict_list)  # map objects are generators, therefore not serializable


def get_filter_string(filter_dict):
    def key_value_pair_to_string(item):
        key, value = item
        return f'{key}={value}'

    return ','.join(map(key_value_pair_to_string, filter_dict.items()))


def get_grouping_aggregation(data):
    n = len(data)
    if n == 0:
        return dict()
    min_value, max_value = data[0].value, data[0].value
    average = 0
    for entry in data:
        min_value = min(min_value, entry.value)
        max_value = max(max_value, entry.value)
        average += entry.value
    average /= n

    standard_dev = 0
    for entry in data:
        standard_dev += (entry.value - average) ** 2
    if n > 1:
        standard_dev = sqrt(standard_dev / (n - 1))

    return {
        'min_group_value': min_value,
        'max_group_value': max_value,
        'average_group_value': average,
        'standard_dev': standard_dev
    }


def get_field_aggregations(queryset, field, numeric_field):
    field_aggregations = {
        'sample_size': Count('pk'),
    }
    if numeric_field:
        field_aggregations.update({
            'min_field_value': Min(field),
            'max_field_value': Max(field),
            'average_field_value': Avg(field),
            'standard_field_deviation': StdDev(field),
        })

    return queryset.aggregate(**field_aggregations)


def generate_distribution(queryset, options):
    field = options.get('field')
    grouping_boundaries = options.get('grouping_boundaries', [])
    group_county = options.get('group_by_county', False)
    group_gender = options.get('group_by_gender', False)
    search_string = options.get('search_string')
    numeric_field = options.get('numeric_field', False)
    filters = options.get('filters', {})

    queryset = queryset.filter(**{f'{field}__isnull': False}).filter(**filters)

    direct_field_aggregation = get_field_aggregations(queryset, field, numeric_field)

    if grouping_boundaries:
        data = get_distribution_by_boundary_grouping(queryset, field, grouping_boundaries)
    elif group_gender:
        data = get_distribution_by_gender_grouping(queryset, field)
    elif group_county:
        data = get_distribution_by_county_grouping(queryset, field)
    else:
        data = get_distribution(queryset, field)

    grouping_values_aggregation = get_grouping_aggregation(data)

    serializable_data = get_serializable_data(data)
    statistics_data = {
        'data': serializable_data,
        'aggregation': {**direct_field_aggregation, **grouping_values_aggregation},
        'meta': {
            'field': options.get('field'),
        }
    }

    group_str = ','.join(map(str, grouping_boundaries))
    filters_str = get_filter_string(options.get('filters', {}))

    statistics_entry, created = Statistic.objects.get_or_create(
        groups=group_str,
        group_by_gender=group_gender,
        group_by_county=group_county,
        field=field,
        filters=filters_str
    )
    json_string = json.dumps(statistics_data, default=json_converter)
    statistics_entry.content = json_string
    statistics_entry.search_string = search_string if search_string else uuid.uuid4()
    statistics_entry.save()
