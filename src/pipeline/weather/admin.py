from django.contrib import admin

from weather.models import WeatherData, Statistics

admin.site.register(WeatherData)
admin.site.register(Statistics)

