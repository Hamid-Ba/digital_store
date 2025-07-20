from django.contrib import admin
from jalali_date.admin import (
    ModelAdminJalaliMixin,
)

from discount import models

# Register your models here.


class DiscountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    """Discount Admin Model"""

    list_display = ["id", "code", "percentage", "start_date", "end_date", "count"]
    list_display_links = ["id", "code", "percentage"]
    list_editable = ["count", "start_date", "end_date"]


admin.site.register(models.DiscountCode, DiscountAdmin)
