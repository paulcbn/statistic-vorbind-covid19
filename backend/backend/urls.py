"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from api_core.views import UtilsView, CreateCaseView, AnalyzeEachCaseTodayView, AnalyzeRawDataView, CollectSourcesView, \
    GenerateDailyStatsView

urlpatterns = [
    path('admin/utils/', UtilsView.as_view()),
    path('admin/internal/create_missing_case/<int:case_number>/', CreateCaseView.as_view()),

    # commands
    path('admin/utils/analyze_each_case_today/', AnalyzeEachCaseTodayView.as_view()),
    path('admin/utils/analyze_raw_data/', AnalyzeRawDataView.as_view()),
    path('admin/utils/collect_sources/<int:page_count>/', CollectSourcesView.as_view()),
    path('admin/utils/generate_daily_stats/', GenerateDailyStatsView.as_view()),

    path('admin/', admin.site.urls),
    path('api/', include('api_core.urls')),
]
