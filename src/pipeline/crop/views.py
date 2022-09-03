from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from crop.filters import CropFilter
from crop.models import CropData
from crop.serializers import CropSerializer


class CropListView(ListAPIView):
    queryset = CropData.objects.all()
    serializer_class = CropSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CropFilter
