from django.db import models

from core.models import BaseModel


class CropData(BaseModel):
    year = models.PositiveSmallIntegerField()
    corn_yield = models.IntegerField()

    class Meta:
        unique_together = ["year", "corn_yield"]
