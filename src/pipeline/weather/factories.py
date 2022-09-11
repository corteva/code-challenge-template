from datetime import date
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat, FuzzyDate, FuzzyInteger

from weather.models import WeatherData, Statistics


class WeatherDataFactory(DjangoModelFactory):
    class Meta:
        model = WeatherData

    station_id = Sequence(lambda n: n)
    date = FuzzyDate(date.fromisoformat("1950-01-01"))
    max_temp = FuzzyFloat(low=0)
    min_temp = FuzzyFloat(low=0)
    precipitation = FuzzyFloat(low=0)


class StatisticsFactory(DjangoModelFactory):
    class Meta:
        model = Statistics

    station_id = Sequence(lambda n: n)
    year = FuzzyInteger(low=1900, high=2200)
    avg_max_temp = FuzzyFloat(low=0)
    avg_min_temp = FuzzyFloat(low=0)
    total_precipitation = FuzzyFloat(low=0)
