from datetime import datetime, date
from django.utils.translation import gettext_lazy as _

from django.db import models


class DiscountCode(models.Model):
    """Discount Code Model"""

    code = models.CharField(max_length=25, null=False, blank=False, verbose_name="کد")
    percentage = models.IntegerField(
        default=0, null=False, blank=False, verbose_name="درصد"
    )
    start_date = models.DateField(null=False, blank=False, verbose_name="زمان شروع")
    end_date = models.DateField(null=False, blank=False, verbose_name="زمان انقضاء")
    count = models.IntegerField(
        default=0, null=False, blank=False, verbose_name="تعداد قابل مصرف"
    )
    reason = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="علت تخفیف"
    )

    def __str__(self) -> str:
        return f"{self.id}-{self.code}"

    def code_used(self):
        self.count -= 1
        self.save()

    def is_code_still_work(self):
        return (
            self.start_date <= date.today()
            and date.today() <= self.end_date
            and self.count > 0
        )

    class Meta:
        verbose_name = _("تخفیف")
        verbose_name_plural = _("تخفیفات")
