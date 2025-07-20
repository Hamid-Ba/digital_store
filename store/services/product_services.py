from store import models, serializers


class ProductServices:
    """Service of Product"""

    def __init__(self) -> None:
        self.products = models.Product.objects.all()

    def get_available_products(self):
        """Return List Of Product With Available Count Greater Than 2"""
        return self.products.all()

    def get_relational_products(self, product_id):
        product = self.products.filter(id=product_id).first()
        return (
            self.products.filter(category=product.category)
            .exclude(id=product_id)
            .order_by("-order_count")
            .values()[:8]
        )
