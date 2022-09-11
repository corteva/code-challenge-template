from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from crop.models import CropData


class CropDataFactory(DjangoModelFactory):
    class Meta:
        model = CropData

    year = Sequence(lambda n: 1950 + n)
    corn_yield = FuzzyInteger(low=0)
