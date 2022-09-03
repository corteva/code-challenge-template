from rest_framework.generics import ListAPIView

from weather.models import WeatherData, Statistics
from weather.serializers import WeatherDataSerializer, StatisticsSerializer


class WeatherListView(ListAPIView):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer


class StatisticsListView(ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
