from django.conf.urls import url
from member import views


urlpatterns = [
    url(r'^login/', views.UserLogin.as_view()),
    url(r'^logout/', views.UserLogout.as_view()),
    url(r'^signup/', views.UserSignUp.as_view()),
]