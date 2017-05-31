from django.conf.urls import url
from name import views

urlpatterns = [
    url(r'^name', views.GetPlayerInfo.as_view()),
]