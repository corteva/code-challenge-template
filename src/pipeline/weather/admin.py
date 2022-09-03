from django.contrib.admin import register, ModelAdmin

from weather.models import WeatherData, Statistics
from weather.services import generate_years_list, calculate_stats


@register(WeatherData)
class WeatherDataAdmin(ModelAdmin):
    list_display = [
        "station_id",
        "date",
        "max_temp",
        "min_temp",
        "precipitation",
    ]
    ordering = ["station_id", "date"]  # todo: apply ordering to apis



@register(Statistics)
class StatisticsAdmin(ModelAdmin):
    list_display = [
        "station_id",
        "year",
        "avg_max_temp",
        "avg_min_temp",
        "total_precipitation",
    ]
    ordering = ["station_id", "year"]
    actions = ["calculate_all_statistics", ]

    def calculate_all_statistics(self, request, queryset):
        years = generate_years_list()
        calculate_stats(years)
        return

    calculate_all_statistics.short_description = "Calculate All Statistics (no obj needed)"

