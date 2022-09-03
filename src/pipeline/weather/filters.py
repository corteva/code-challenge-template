from django_filters import FilterSet, CharFilter, DateFilter

from weather.models import WeatherData, Statistics


# todo: which filters can be moved to common or outside of class
# todo: reevaluate types of filters and if all should be done in Meta.fields


class WeatherFilter(FilterSet):
    date = DateFilter
    station_id = CharFilter(lookup_expr="iexact")

    class Meta:
        model = WeatherData
        fields = ["year", "station_id"]


class StatisticsFilter(FilterSet):
    year = CharFilter(lookup_expr="iexact")
    station_id = CharFilter(lookup_expr="iexact")

    class Meta:
        model = Statistics
        fields = ["year", "station_id"]
