from store import models
from django.shortcuts import get_object_or_404


class OrderServices:
    """Service of Order"""

    def __init__(self) -> None:
        self.orders = models.Order.objects.all()

    def reduction_inventory(self, order_id):
        order = get_object_or_404(models.Order, pk=order_id)
        order_items = order.items.all()

        if order.discount:
            code = order.discount
            code.code_used()

        for item in order_items:
            product_item = models.Product.objects.filter(id=item.product_id)
            if product_item.exists():
                product_item.first().ordered(item.count)

    def delete_order(self, order_id):
        models.Order.objects.filter(id=order_id).delete()
