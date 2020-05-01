from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from rest_framework import generics
from rest_framework import permissions

from api_core.models import Statistic, Case
from api_core.serializers import StatisticSerializer


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
        context.update({
            "user": self.request.user,
            "has_permission": True,
            "is_popup": False,
            "available_apps": admin.site.each_context(self.request)["available_apps"],
            "title": "Utils",
            "missing_cases": self.get_missing_cases(),
        })
        return context


class CreateCaseView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            case_number = self.kwargs["case_number"]
            case = Case.objects.create(case_number=case_number, collision_index=1)
            return f"/admin/api_core/case/{case.id}/change/"
        else:
            return "/admin/"
