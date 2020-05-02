from django.contrib import admin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, RedirectView
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from api_core.models import Statistic, Case
from api_core.pagination import DefaultPagination
from api_core.serializers import StatisticSerializer, CaseSerializer
from data_parsing.services.case_analyzer.case_analyzer_service import analyze_all_cases
from data_parsing.services.raw_data_analyzer_service import create_deaths_from_data_sources
from data_parsing.services.sources_collector_service import collect_data_sources
from data_parsing.services.statistics.daily import generate_daily_statistics


class StatisticView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StatisticSerializer
    lookup_url_kwarg = 'search_string'
    lookup_field = 'search_string'

    def get_queryset(self):
        return Statistic.objects.all()


class UtilsView(TemplateView):
    template_name = "admin/utils_template.html"

    def get_missing_cases(self):
        ordered_cases = Case.objects.order_by('case_number')
        last_case_number = ordered_cases.last().case_number
        cases = Case.objects.all()
        missing_cases_numbers = []
        for case_number in range(1, last_case_number):
            if not cases.filter(case_number=case_number).exists():
                missing_cases_numbers.append(case_number)
        return missing_cases_numbers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        missing_cases = self.get_missing_cases()
        context.update({
            "user": self.request.user,
            "has_permission": True,
            "is_popup": False,
            "available_apps": admin.site.each_context(self.request)["available_apps"],
            "title": "Utils",
            "missing_cases": missing_cases,
            "missing_cases_intervals": self.make_intervals(missing_cases)
        })
        return context

    def make_intervals(self, numeric_list):
        intervals = list()
        if len(numeric_list) == 0:
            return intervals
        start = 0
        for i in range(len(numeric_list) - 1):
            if numeric_list[i + 1] - numeric_list[i] != 1 and i > start:
                intervals.append((numeric_list[start], numeric_list[i]))
                start = i + 1
            elif numeric_list[i + 1] - numeric_list[i] != 1:
                intervals.append((numeric_list[i], numeric_list[i]))
                start = i + 1
        if start < len(numeric_list) - 1:
            intervals.append((numeric_list[start], numeric_list[-1]))
        return [f"Cazurile {interval[0]} - {interval[1]}" for interval in intervals]


class AnalyzeEachCaseTodayView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            analyze_all_cases(today=True)
            return HttpResponse(status=200)
        return HttpResponse(status=401)


class AnalyzeRawDataView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            create_deaths_from_data_sources(today=True)
            return HttpResponse(status=200)
        return HttpResponse(status=401)


class CollectSourcesView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                pages = int(kwargs["page_count"])
                collect_data_sources(base_url="https://stirioficiale.ro/informatii", page_count=pages)
                return HttpResponse(status=200)
            except Exception:
                return HttpResponse(status=400)
        return HttpResponse(status=401)


class GenerateDailyStatsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            generate_daily_statistics()
            return HttpResponse(status=200)
        return HttpResponse(status=401)


class CreateCaseView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            case_number = self.kwargs["case_number"]
            case = Case.objects.create(case_number=case_number, collision_index=1)
            return f"/admin/api_core/case/{case.id}/change/"
        else:
            return "/admin/"


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Case
        fields = {
            'case_number': ['exact', ],  # usage example: ?case_number=233
            'collision_index': ['exact', ],
            'date_created': ['gte', 'lte', 'gt', 'lt'],  # usage example: ?date_created__gte=2020-01-01T00:00:00Z
            'date_modified': ['gte', 'lte', 'gt', 'lt'],
            'gender': ['exact', ],  # usage example: ?gender=F
            'age': ['gte', 'lte', 'gt', 'lt'],
            'county': ['icontains'],
            'hospital_admission_date': ['gte', 'lte', 'gt', 'lt'],
            'test_date': ['gte', 'lte', 'gt', 'lt'],
            'positive_result_date': ['gte', 'lte', 'gt', 'lt'],
            'death_date': ['gte', 'lte', 'gt', 'lt'],
            'source__url': ['exact', ],
            'comorbidities__name': ['icontains', ],
            'initial_hospital__name': ['icontains', ],
            'final_hospital__name': ['icontains', ],  # usage example: ?final_hospital__name__icontains=Covasna
            'validated': ['exact', ]
        }


class CaseView(ListAPIView):
    serializer_class = CaseSerializer
    pagination_class = DefaultPagination
    queryset = Case.objects.order_by("case_number", "collision_index").all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
