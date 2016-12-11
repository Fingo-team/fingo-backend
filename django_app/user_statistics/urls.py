from django.conf.urls import url
from user_statistics import views

urlpatterns = [
    url(r"scores/$", views.StatisticsScores.as_view()),
    url(r"actors/$", views.StatisticsActors.as_view()),
    url(r"directors/$", views.StatisticsDirectors.as_view()),
    url(r"genres/$", views.StatisticsGenres.as_view()),
    url(r"nations/$", views.StatisticsNations.as_view()),
    url(r"all/$", views.StatisticsAll.as_view()),
]
