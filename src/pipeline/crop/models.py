from django.db import models

from core.models import BaseModel


class CropData(BaseModel):
    year = models.PositiveSmallIntegerField(
        unique=True, help_text="Year of the harvest"
    )
    corn_yield = models.IntegerField(
        help_text="Corn grain yield in the United States (measured in 1000s of megatons)"
    )
