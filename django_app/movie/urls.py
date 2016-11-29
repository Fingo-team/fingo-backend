from django.conf.urls import url
from movie import views

urlpatterns = [
    url(r"detail/(?P<pk>\d+)/$", views.MovieDetail.as_view()),
    url(r"rank/$", views.BoxofficeRankList.as_view())
]