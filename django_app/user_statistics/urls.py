from django.conf.urls import url
from user_statistics import views

urlpatterns = [
    url(r"scores/$", views.StatisticsScores.as_view()),
    url(r"actors/$", views.StatisticsActors.as_view()),
]