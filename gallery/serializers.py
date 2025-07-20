"""
Gallery Module Serializer
"""

from rest_framework import serializers

from gallery import models


class GallerySerializer(serializers.ModelSerializer):
    """Gallery Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Gallery
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["url"] = instance.image.url

        return rep
