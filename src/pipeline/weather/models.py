from django.db import models

from core.constants import MISSING_VALUE
from core.models import BaseModel


class WeatherData(BaseModel):
    """
    WeatherData model stores data collected daily from weather stations.
    """

    station_id = models.CharField(max_length=50, help_text="Weather station identifier")
    date = models.DateField(help_text="Date of data collection")
    max_temp = models.FloatField(
        default=MISSING_VALUE,
        help_text="Highest temperature recorded for the day (measured in degrees Celsius)",
    )
    min_temp = models.FloatField(
        default=MISSING_VALUE,
        help_text="Lowest temperature recorded for the day (measured in degrees Celsius)",
    )
    precipitation = models.FloatField(
        default=MISSING_VALUE,
        help_text="Amount of precipitation recorded for the day (measured in centimeters)",
    )

    class Meta:
        unique_together = [
            "station_id",
            "date",
        ]


class Statistics(BaseModel):
    """
    Statistics model stores basic stats calculated from subsets of WeatherData .
    """

    station_id = models.CharField(max_length=50, help_text="Weather station identifier")
    year = models.PositiveSmallIntegerField(
        help_text="Year that the statistics were calculated for"
    )
    avg_max_temp = models.FloatField(
        null=True,
        help_text="Average of the daily max temperatures recorded (measured in degrees Celsius)",
    )
    avg_min_temp = models.FloatField(
        null=True,
        help_text="Average of the daily min temperatures recorded (measured in degrees Celsius)",
    )
    total_precipitation = models.FloatField(
        null=True,
        help_text="Sum of the daily precipitation recorded (measured in centimeters)",
    )

    class Meta:
        unique_together = [
            "station_id",
            "year",
        ]
