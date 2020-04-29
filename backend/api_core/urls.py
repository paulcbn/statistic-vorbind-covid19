from django.conf.urls import url
from django.urls import include, path

from api_core.views import StatisticsView

urlpatterns = [
    url(r'^statistics', StatisticsView.as_view(), name='app_gallery'),
]
