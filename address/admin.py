from django.contrib import admin

from address import models


# Register your models here.
class AddressAdminModel(admin.ModelAdmin):
    """Address Admin Model"""

    list_display = ["user", "province", "city", "postal_code"]
    list_display_link = ["user", "postal_code"]


admin.site.register(models.Address, AddressAdminModel)
