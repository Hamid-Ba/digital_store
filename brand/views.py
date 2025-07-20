from rest_framework import generics

from brand import models, serializers


# Create your views here.
class BrandsApiView(generics.ListAPIView):
    """Return List Of Brands"""

    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    # pagination_class = pagination.StandardPagination
