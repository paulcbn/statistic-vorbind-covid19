from rest_framework import serializers
from rest_framework.utils import json

from api_core.models import Statistic, Case, Hospital, Comorbidity, DataSource


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['search_string', 'date_modified', 'content']

    content = serializers.SerializerMethodField()

    def get_content(self, item):
        return json.loads(item.content)


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['name', ]


class ComorbiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comorbidity
        fields = ['name', ]


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['url', ]


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        initial_hospital = HospitalSerializer(read_only=True, many=False)
        final_hospital = HospitalSerializer(read_only=True, many=False)
        comorbidities = ComorbiditySerializer(read_only=True, many=True)
        source = DataSourceSerializer(read_only=True, many=False)
        fields = ['case_number', 'collision_index', 'date_created', 'date_modified', 'gender', 'age', 'county',
                  'hospital_admission_date', 'test_date', 'positive_result_date', 'death_date', 'source',
                  'comorbidities', 'initial_hospital', 'final_hospital']
