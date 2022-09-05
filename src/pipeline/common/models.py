from django.db import models


class BaseModel(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        abstract = True
