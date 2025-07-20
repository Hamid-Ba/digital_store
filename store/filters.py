from django_filters import FilterSet, RangeFilter

from store import models


class PriceRangeFilter(FilterSet):
    price = RangeFilter()

    class Meta:
        model = models.Product
        fields = ["price"]
