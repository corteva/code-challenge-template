from django.urls import path

from weather.views import WeatherListView, StatisticsListView


urlpatterns = [
    path("", WeatherListView.as_view(), name="weather_list"),
    path("/stats", StatisticsListView.as_view(), name="stats_list"),
]
