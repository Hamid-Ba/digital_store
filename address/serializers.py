from rest_framework import serializers

from address import models


class AddressSerializer(serializers.ModelSerializer):
    """Address Serializer"""

    class Meta:
        model = models.Address
        fields = "__all__"
        read_only_fields = ["user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        try:
            rep["user"] = instance.user.phone
            rep["province"] = instance.province.name
            rep["city"] = instance.city.name
        except:
            pass

        return rep
