from django.urls import path
from contest import views

urlpatterns = [
    path('', views.ContestManager.as_view()),
]