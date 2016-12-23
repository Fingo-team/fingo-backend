from django.conf.urls import url
from fingo_statistics import views


urlpatterns = [
    url(r"user/detail/$", views.UserDetailView.as_view()),
    url(r"user/comments/$", views.UserCommentsSelect.as_view()),
    url(r"user/wish/movies/$", views.UserWishMoviesSelect.as_view()),
    url(r"user/watched/movies/$", views.UserWatchedMoviesSelect.as_view()),
    # url(r"user/watched_movies/$", views.UserDetailView.as_view()),
]