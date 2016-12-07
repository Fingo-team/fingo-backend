from django.conf.urls import url
from fingo_statistics import views


urlpatterns = [
    url(r"user/detail/$", views.UserDetailView.as_view()),
    url(r"user/comments/$", views.UserComments.as_view()),
    # url(r"user/watched_movies/$", views.UserDetailView.as_view()),
]