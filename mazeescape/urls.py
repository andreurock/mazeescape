from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('name.urls')),
    url(r'^', include('move.urls')),
]