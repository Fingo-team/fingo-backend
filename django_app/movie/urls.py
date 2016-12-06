from django.conf.urls import url
from movie import views

urlpatterns = [
    url(r"detail/(?P<pk>\d+)/$", views.MovieDetail.as_view()),
    url(r"detail/(?P<pk>\d+)/comments/$", views.MovieComment.as_view()),
    url(r"boxoffice/$", views.BoxofficeRankList.as_view()),
    url(r"search/", views.MovieSearch.as_view()),
    url(r"score/(?P<pk>\d+)/$", views.MovieScore.as_view()),
]