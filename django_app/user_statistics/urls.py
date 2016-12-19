from django.conf.urls import url
from user_statistics import views

urlpatterns = [
    url(r"all/$", views.StatisticsAll.as_view()),
]
