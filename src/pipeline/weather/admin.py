from django.contrib.admin import register, ModelAdmin

from weather.models import WeatherData, Statistics


@register(WeatherData)
class WeatherDataAdmin(ModelAdmin):
    list_display = (
        "station_id",
        "date",
        "max_temp",
        "min_temp",
        "precipitation",
    )


@register(Statistics)
class StatisticsAdmin(ModelAdmin):
    list_display = (
        "station_id",
        "year",
        "avg_max_temp",
        "avg_min_temp",
        "total_precipitation",
    )


