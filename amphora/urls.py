from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("api/", include("amphora.api.urls")),
    path("", include("amphora.health.urls")),
    path("admin/", admin.site.urls),
]
