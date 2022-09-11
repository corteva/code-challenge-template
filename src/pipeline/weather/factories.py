from datetime import date

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat, FuzzyDate, FuzzyInteger

from weather.models import WeatherData, Statistics


class WeatherDataFactory(DjangoModelFactory):
    class Meta:
        model = WeatherData

    station_id = FuzzyText(length=30)
    date = FuzzyDate(date.fromisoformat("1950-01-01"))
    max_temp = FuzzyFloat(low=0)
    min_temp = FuzzyFloat(low=0)
    precipitation = FuzzyFloat(low=0)


class StatisticsFactory(DjangoModelFactory):
    class Meta:
        model = Statistics

    station_id = FuzzyText(length=30)
    year = FuzzyInteger(low=1900, high=2200)
    avg_max_temp = FuzzyFloat(low=0)
    avg_min_temp = FuzzyFloat(low=0)
    total_precipitation = FuzzyFloat(low=0)

