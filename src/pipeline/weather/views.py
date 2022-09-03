from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from weather.filters import WeatherFilter, StatisticsFilter
from weather.models import WeatherData, Statistics
from weather.serializers import WeatherDataSerializer, StatisticsSerializer


class WeatherListView(ListAPIView):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WeatherFilter


class StatisticsListView(ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StatisticsFilter
