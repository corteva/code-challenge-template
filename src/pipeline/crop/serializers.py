from rest_framework import serializers

from crop.models import CropData


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropData
        fields = ['year', 'corn_yield']
