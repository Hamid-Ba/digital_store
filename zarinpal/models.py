"""
Payment Models Module
"""
from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from store import models as store_models


class Payment(models.Model):
    """Payment Model"""

    class PaymentStatus(models.IntegerChoices):
        """Payment Status Enums"""

        PAYMENT_CREATED = 1, "در حال پرداخت"
        PAYMENT_DONE = 2, "پرداخت انجام شد"
        PAYMENT_CANCELLED = 3, "پرداخت لغو شد"

    pay_amount = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False, verbose_name="مبلغ پرداختی"
    )
    desc = models.CharField(max_length=125, null=True, blank=True, verbose_name="توضیحات")
    ref_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="شناسه پرداخت")
    authority = models.CharField(max_length=50, null=True, blank=True, verbose_name="کد پرداخت")
    is_payed = models.BooleanField(default=False, verbose_name="آیا پرداخت شده؟")
    payed_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ پرداخت")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.PAYMENT_CREATED, verbose_name="وضعیت"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="کاربر"
    )
    order = models.ForeignKey(
        store_models.Order, on_delete=models.CASCADE, related_name="payments", verbose_name="سفارش"
    )

    def __str__(self) -> str:
        return f"User Phone : {self.user.phone}"
    
    class Meta:
        verbose_name = _("فاکتور")
        verbose_name_plural = _("فاکتور ها")
