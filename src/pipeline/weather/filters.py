from django_filters.rest_framework import FilterSet, CharFilter, DateFilter

from weather.models import WeatherData, Statistics


class WeatherFilter(FilterSet):
    date = DateFilter(field_name="date", lookup_expr="iexact")
    station_id = CharFilter(field_name="station_id", lookup_expr="iexact")

    class Meta:
        model = WeatherData
        fields = ["date", "station_id"]


class StatisticsFilter(FilterSet):
    year = CharFilter(field_name="year", lookup_expr="iexact")
    station_id = CharFilter(field_name="station_id", lookup_expr="iexact")

    class Meta:
        model = Statistics
        fields = ["year", "station_id"]
