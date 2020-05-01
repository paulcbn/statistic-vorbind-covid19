from django.urls import path

from api_core.views import StatisticView, CaseView

urlpatterns = [
    path('statistics/<str:search_string>/', StatisticView.as_view()),
    path('case/', CaseView.as_view()),
]
