from django.conf.urls import url
from fingo_statistics import views


urlpatterns = [
    url(r"userdetail/$", views.UserDetailView.as_view())
]