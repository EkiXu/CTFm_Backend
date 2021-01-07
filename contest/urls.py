from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from contest import views

urlpatterns = [
    path('contest/', views.ContestManager.as_view()),
    path('admin/contest/', views.AdminContestManager.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)