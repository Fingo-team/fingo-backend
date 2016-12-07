from django.conf.urls import url
from movie import views

urlpatterns = [
    # movie detail
    url(r"detail/(?P<pk>\d+)/$", views.MovieDetail.as_view()),
    url(r"detail/(?P<pk>\d+)/comments/$", views.MovieComments.as_view()),
    # boxoffice
    url(r"boxoffice/$", views.BoxofficeRankList.as_view()),
    # search
    url(r"search/", views.MovieSearch.as_view()),
    # score
    url(r"score/(?P<pk>\d+)/$", views.MovieScore.as_view()),
    # comment
    url(r"(?P<pk>\+d)/comment/$", views.MovieAsUserComment.as_view()),
    # wish
    url(r"wish/(?P<pk>\d+)/$", views.MovieWish.as_view()),
]