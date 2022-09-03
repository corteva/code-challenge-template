from rest_framework import serializers

from weather.models import WeatherData, Statistics


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['date', 'max_temp', 'min_temp', 'precipitation']


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['year', 'avg_max_temp', 'avg_min_temp', 'total_precipitation']
