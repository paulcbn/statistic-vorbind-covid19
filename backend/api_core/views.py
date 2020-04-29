from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView

from api_core.models import Statistics


class StatisticsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        field = request.query_params.get('field')
        group_gender = request.query_params.get('group_gender', False)
        group_county = request.query_params.get('group_county', False)

        # groups can be "18,40,70"
        groups = request.query_params.get('group')

        # filters can be "age__gt:18,age_lt:30"
        filters = request.query_params.get('filters')

        statistics = Statistics.objects.filter(group_by_county=group_county,
                                               group_by_gender=group_gender,
                                               field=field)
        if groups:
            statistics = statistics.filter(groups=groups)

        if filters:
            statistics = statistics.filter(filters=filters)

        statistics_entry = statistics.first()

        if not statistics_entry:
            return HttpResponseNotFound()
        return JsonResponse(statistics_entry.content)
