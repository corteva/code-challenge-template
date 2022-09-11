from django.urls import path

from weather.views import WeatherListView, StatisticsListView


urlpatterns = [
    path("weather", WeatherListView.as_view(), name="weather_list"),
    path("weather/stats", StatisticsListView.as_view(), name="stats_list"),
]
