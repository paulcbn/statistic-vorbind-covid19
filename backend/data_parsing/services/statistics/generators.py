import json
from datetime import datetime

from django.db.models import Max, Avg, Count, Min

from api_core.models import Statistics


def generate_distribution(queryset, options):
    # used to be really general, now it's mostly stuck doing Case
    field = options.get('fields')[0]
    groups = options.get('group')
    group_county = options.get('group_by_county')
    group_gender = options.get('group_by_gender')

    aggregation = queryset.aggregate(min=Min(field), max=Max(field), average=Avg(field))

    def get_group(value):
        if value <= groups[0]:
            return 0
        for j in range(0, len(groups) - 1):
            if groups[j] < value <= groups[j + 1]:
                return j + 1
        return len(groups)

    if groups:
        data = [{
            'key': 0,
            'count': 0,
            'label': f"sub {groups[0]}"
        }]
        for group_id in range(0, len(groups) - 1):
            data.append({
                'key': group_id + 1,
                'count': 0,
                'label': f"{groups[group_id]} - {groups[group_id + 1]}",
            })

        data.append({
            'key': group_id,
            'count': 0,
            'label': f"peste {groups[-1]}",
        })

        for a in queryset.values(field).annotate(count=Count(field)).all():
            data[get_group(a[field])]['count'] = data[get_group(a[field])]['count'] + 1

    elif group_gender:
        males = []
        females = []

        for a in queryset.values(field).annotate(count=Count(field)).all():
            if a.gender == queryset.model.MALE:
                males.append({a[field]: a['count']})
            else:
                females.append({a[field]: a['count']})

        data = [
            {
                'males': males
            },
            {
                'females': females
            }
        ]

    elif group_county:
        counties = {}
        # TODO: implement this.
        # for a in queryset.values(field).annotate(count=Count(field)).all():
        #     if a.county in counties.keys():
        #         counties[a.county]
    else:
        data = [{a[field]: a['count']} for a in queryset.values(field).annotate(count=Count(field)).all()]

    statistics = {
        'data': data,
        'aggregation': aggregation,
        'meta': {
            'model': options.get('model'),
            'fields': options.get('fields'),
            'normalized': options.get('normalize'),
            'type': options.get('type'),
            'filters': options.get('filters'),
        }
    }

    group_str = str(groups)[1:-1].replace(' ', '')
    filters_str = str(options.get('filters'))[1:-1].replace("'", "").replace(' ', '')
    statistics_entry = Statistics.objects.get(
        groups=group_str,
        group_by_gender=group_gender,
        group_by_county=group_county,
        field=field,
        filters=filters_str
    )
    if statistics_entry:
        print("Replacing old statistics")
        statistics_entry.update(
            content=data,
            date_created=datetime.now(),
            groups=group_str,
            group_by_gender=group_gender,
            group_by_county=group_county,
            field=field,
            filters=filters_str
        )
        return

    Statistics.objects.create(
        content=data,
        date_created=datetime.now(),
        groups=group_str,
        group_by_gender=group_gender,
        group_by_county=group_county,
        field=field,
        filters=filters_str
    )
    print(f"Generated {statistics}")
