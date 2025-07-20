from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.db import models
from province import models as province_model


class Address(models.Model):
    """Address Model"""

    full_name = models.CharField(
        max_length=225, null=False, blank=False, verbose_name="نام کامل"
    )
    desc = models.CharField(
        max_length=225, null=True, blank=True, verbose_name="توضیحات"
    )
    street = models.CharField(
        max_length=225, null=True, blank=True, verbose_name="خیابان"
    )
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="کاربر",
    )
    province = models.ForeignKey(
        province_model.Province, on_delete=models.DO_NOTHING, verbose_name="استان"
    )
    city = models.ForeignKey(
        province_model.City, on_delete=models.DO_NOTHING, verbose_name="شهر"
    )

    def __str__(self) -> str:
        return f"{self.full_name} - {self.postal_code}"

    class Meta:
        verbose_name = _("نشانی")
        verbose_name_plural = _("نشانی ها")
