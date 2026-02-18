from django.urls import path

from amphora.api import views

urlpatterns = [
    path("access-points/", views.AccessPointsEndpoint.as_view(), name="access-points"),
]
