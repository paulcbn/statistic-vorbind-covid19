from rest_framework import serializers
from rest_framework.utils import json

from api_core.models import Statistic


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['search_string', 'date_modified', 'content']

    content = serializers.SerializerMethodField()

    def get_content(self, item):
        return json.loads(item.content)
