from rest_framework import permissions
from rest_framework import generics

from api_core.models import Statistic
from api_core.serializers import StatisticSerializer


class StatisticView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StatisticSerializer
    lookup_url_kwarg = 'search_string'
    lookup_field = 'search_string'

    def get_queryset(self):
        return Statistic.objects.all()
