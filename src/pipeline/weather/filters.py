from django_filters.rest_framework import FilterSet, CharFilter, DateFilter

from weather.models import WeatherData, Statistics


# todo: which filters can be moved to core or outside of class
# todo: reevaluate types of filters and if all should be done in Meta.fields


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
