from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from core.models import BaseModel


class CropData(BaseModel):
    """
    CropData model is used to store crop yield data in the United States by year
    """

    year = models.PositiveSmallIntegerField(
        unique=True, help_text="Year of the harvest"
    )
    corn_yield = models.IntegerField(
        help_text="Corn grain yield in the United States (measured in 1000s of megatons)"
    )

    objects = BulkUpdateOrCreateQuerySet.as_manager()
