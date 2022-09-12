from django.db import models

from core.models import BaseModel


class WeatherData(BaseModel):
    station_id = models.CharField(max_length=50, help_text="Weather station identifier")
    date = models.DateField(help_text="Date of data collection")
    max_temp = models.FloatField(help_text="Highest temperature recorded for the day (measured in degrees Celsius)")
    min_temp = models.FloatField(help_text="Lowest temperature recorded for the day (measured in degrees Celsius)")
    precipitation = models.FloatField(help_text="Amount of precipitation recorded for the day (measured in centimeters)")

    class Meta:
        unique_together = [
            "station_id",
            "date",
            "max_temp",
            "min_temp",
            "precipitation",
        ]


class Statistics(BaseModel):
    station_id = models.CharField(max_length=50, help_text="Weather station identifier")
    year = models.PositiveSmallIntegerField(help_text="Year that the statistics were calculated for")
    avg_max_temp = models.FloatField(null=True, help_text="Average of the daily max temperatures recorded (measured in degrees Celsius)")
    avg_min_temp = models.FloatField(null=True, help_text="Average of the daily min temperatures recorded (measured in degrees Celsius)")
    total_precipitation = models.FloatField(null=True, help_text="Sum of the daily precipitation recorded (measured in centimeters)")
