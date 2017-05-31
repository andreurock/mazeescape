from django.conf.urls import url
from move import views

urlpatterns = [
    url(r'^move', views.Move.as_view()),
]