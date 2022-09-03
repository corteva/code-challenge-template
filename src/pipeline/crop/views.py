from rest_framework.generics import ListAPIView

from crop.models import CropData
from crop.serializers import CropSerializer


class CropListView(ListAPIView):
    queryset = CropData.objects.all()
    serializer_class = CropSerializer

