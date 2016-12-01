from django.conf.urls import url
from member import views


urlpatterns = [
    url(r'^login/$', views.UserLogin.as_view()),
    url(r'^logout/$', views.UserLogout.as_view()),
    url(r'^signup/$', views.UserSignUp.as_view()),
    url(r'^activate/(?P<useremail>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.UserActivate.as_view()),
]