from django.db import models

from core.models import BaseModel


class WeatherData(BaseModel):
    station_id = models.CharField(max_length=50)
    date = models.DateField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    precipitation = models.FloatField()

    class Meta:
        unique_together = [
            "station_id",
            "date",
            "max_temp",
            "min_temp",
            "precipitation",
        ]


class Statistics(BaseModel):
    station_id = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)
