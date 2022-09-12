from django.contrib.admin import register, ModelAdmin

from crop.models import CropData


@register(CropData)
class CropDataAdmin(ModelAdmin):
    list_display = ["year", "corn_yield"]
    list_filter = [
        "year",
    ]
    ordering = [
        "year",
    ]
