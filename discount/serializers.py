from uuid import uuid4
from rest_framework import serializers

from discount import models


class DiscountSerializer(serializers.ModelSerializer):
    """Discount Serializer"""

    class Meta:
        model = models.DiscountCode
        fields = "__all__"
