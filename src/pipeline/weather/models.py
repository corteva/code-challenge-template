from django.db import models

from common.models import BaseModel


class WeatherData(BaseModel):
    station_id = models.CharField(max_length=50)
    date = models.DateField()
    max_temp = models.DecimalField(max_digits=4, decimal_places=1)
    min_temp = models.DecimalField(max_digits=4, decimal_places=1)
    precipitation = models.DecimalField(max_digits=4, decimal_places=1)

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
