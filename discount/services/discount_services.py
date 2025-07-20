from discount import models
from store import models as store_models


class DiscountServices:
    """Discount Services"""

    def __init__(self) -> None:
        self.discounts = models.DiscountCode.objects.all()

    def get_discount_by(self, code):
        return self.discounts.filter(code=code).first()

    def is_discount_code_valid(self, code, user):
        code = models.DiscountCode.objects.filter(code=code)

        if code.exists():
            code = code.first()
            if not store_models.Order.objects.filter(user=user, discount=code).exists():
                if code.is_code_still_work():
                    return code

        return False
