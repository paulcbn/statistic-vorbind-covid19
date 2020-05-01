from django.urls import path

from api_core.views import StatisticView

urlpatterns = [
    path('statistics/<str:search_string>/', StatisticView.as_view()),
]
