from django.urls import path
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from contest import views

urlpatterns = [
    path('contest/', views.ContestManager.as_view()),
    path('contest/trend/',views.TopTenTrendView.as_view(), name='Contest Trend'),
    path('contest/scoreboard/',views.ScoreboardView.as_view(), name='Contest Scoreboard'),
    path('contest/trend/team/',views.TopTenTeamTrendView.as_view(), name='Contest Team Trend'),
    path('contest/scoreboard/team/',views.TeamScoreboardView.as_view(), name='Contest Team Scoreboard'),
    path('admin/contest/', views.AdminContestManager.as_view()),
]

if settings.ENABLE_SCHOOL_RANKING:
    urlpatterns.extend([
        path('contest/trend/stu/',views.StuTopTenTrendView.as_view(), name='Stu Contest Trend'),
        path('contest/scoreboard/stu/',views.StuScoreboardView.as_view(), name='Stu Contest Scoreboard'),
    ])

urlpatterns = format_suffix_patterns(urlpatterns)