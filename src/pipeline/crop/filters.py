from django_filters import FilterSet, CharFilter

from crop.models import CropData


class CropFilter(FilterSet):
    year = CharFilter(field_name="year", lookup_expr="iexact")  # todo: Number filter?

    class Meta:
        model = CropData
        fields = ["year"]
