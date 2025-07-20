from rest_framework import serializers

from brand import models


class BrandSerializer(serializers.ModelSerializer):
    """Brand Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Brand
        fields = "__all__"
