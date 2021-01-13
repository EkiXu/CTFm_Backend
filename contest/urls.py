from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from contest import views

urlpatterns = [
    path('contest/', views.ContestManager.as_view()),
    path('contest/trend/',views.getTopTenTrend, name='Contest Trend'),
    path('contest/scoreboard/',views.getScoreBoard, name='Contest Scoreboard'),
    path('admin/contest/', views.AdminContestManager.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)