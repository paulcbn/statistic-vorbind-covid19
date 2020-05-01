from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from api_core.models import Statistic, Case
from api_core.pagination import DefaultPagination
from api_core.serializers import StatisticSerializer, CaseSerializer


class StatisticView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StatisticSerializer
    lookup_url_kwarg = 'search_string'
    lookup_field = 'search_string'

    def get_queryset(self):
        return Statistic.objects.all()


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
        }


class CaseView(ListAPIView):
    serializer_class = CaseSerializer
    pagination_class = DefaultPagination
    queryset = Case.objects.order_by("case_number", "collision_index").all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
