import json
from uuid import uuid4
from rest_framework import serializers
from django.core.serializers import serialize

from store import models
from brand import serializers as brand_serial
from gallery import serializers as gallery_serial
from address import serializers as address_serial


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Category
        fields = "__all__"


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        """Meta Class"""

        model = models.Category
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["subs"] = []

        if instance.sub_categories.exists():
            rep["subs"] = instance.sub_categories.order_by("-order").values()

        return rep


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Comment
        fields = "__all__"
        read_only_fields = ["user", "is_active"]


class SpecificationsSerializer(serializers.ModelSerializer):
    """Specifications Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Specifications
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    """Product Serializer"""

    category = CategorySerializer(many=False)
    brand = brand_serial.BrandSerializer(many=False)
    gallery = gallery_serial.GallerySerializer(many=True)

    class Meta:
        """Meta Class"""

        model = models.Product
        fields = [
            "id",
            "title",
            "price",
            "short_desc",
            "category",
            "brand",
            "gallery",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Product Serializer"""

    category = CategorySerializer(many=False)
    brand = brand_serial.BrandSerializer(many=False)
    gallery = gallery_serial.GallerySerializer(many=True)
    specs = SpecificationsSerializer(many=True)
    comments = CommentSerializer(many=True)

    domain = serializers.SerializerMethodField()

    def get_domain(self, obj):
        request = self.context.get("request")
        url = request.build_absolute_uri(obj.pk).split("/")
        url = f"{url[0]}//{url[2]}"
        return url

    class Meta:
        """Meta Class"""

        model = models.Product
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        relational_products = (
            models.Product.objects.get_relational_products_by_category(
                instance.id, instance.category.id
            )
        )
        rep["comments"] = instance.get_active_comments()
        rep["relational_products"] = []
        [
            rep["relational_products"].append(ProductListSerializer(instance=prod).data)
            for prod in relational_products
            if len(relational_products)
        ]

        return rep


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Payment Method Serializer"""

    class Meta:
        model = models.PaymentMethod
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """Order Item Serializer"""

    class Meta:
        model = models.OrderItem
        fields = "__all__"
        read_only_fields = ("order",)


class CreateOrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""

    items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = "__all__"
        read_only_fields = ("user", "code", "state")

    def _add_items(self, order, items):
        for item in items:
            product_id = item["product_id"]
            count = item["count"]
            product_item = models.Product.objects.filter(id=product_id)

            if product_item.exists():
                if not product_item.first().can_order(count):
                    models.Order.objects.filter(id=order.id).delete()
                    raise ValueError(
                        f"تعداد محصول درخواستی {product_item.first().title} در انبار موجود نمی باشد"
                    )

        for item in items:
            order.items.create(
                product_id=item["product_id"],
                brand=item["brand"],
                title=item["title"],
                # image_url=item["image_url"],
                price=item["price"],
                count=item["count"],
            )

            # product_item = models.Product.objects.filter(id=item["product_id"])
            # if product_item.exists():
            #     product_item.first().ordered(item["count"])

    def create(self, validated_data):
        """Custom Create"""
        items = validated_data.pop("items", [])
        # code = str(uuid4())[:5]

        code = str(models.Order.objects.count())

        order = models.Order.objects.create(code=code, **validated_data)
        self._add_items(order, items)
        order.save()

        return order


class OrderSerializer(CreateOrderSerializer):
    """Create Order Serialzier"""

    address = address_serial.AddressSerializer(many=False)
    payment_method = PaymentMethodSerializer(many=False)


class CreateFavoriteProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all())

    class Meta:
        model = models.FavoriteProduct
        fields = "__all__"
        read_only_fields = ["user"]


class FavoriteProductSerializer(CreateFavoriteProductSerializer):
    product = ProductListSerializer(many=False)

    class Meta(CreateFavoriteProductSerializer.Meta):
        pass
