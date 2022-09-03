from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Challenge Solution Admin Pages"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/weather", include("weather.urls")),
    path("api/yield", include("crop.urls")),
]
