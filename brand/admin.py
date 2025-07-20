from brand import models
from django.contrib import admin


# Register your models here.
class BrandAdminModel(admin.ModelAdmin):
    """Brand Admin Model"""

    list_display = ["id", "title", "logo"]
    list_display_links = ["id", "title"]


admin.site.register(models.Brand, BrandAdminModel)
