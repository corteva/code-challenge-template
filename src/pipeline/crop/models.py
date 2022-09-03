from django.db import models


class CropData(models.Model):
    year = models.PositiveSmallIntegerField()
    corn_yield = models.IntegerField()

    class Meta:
        unique_together = ['year', 'corn_yield']
