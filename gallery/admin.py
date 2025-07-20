from django.contrib import admin

from gallery import models

# Register your models here.


class GalleryAdmin(admin.ModelAdmin):
    """Gallery Admin Model"""

    list_display = ["id", "title", "image_path"]
    list_display_links = ["id", "title"]
    sortable_by = ["title"]
    search_fields = ["title"]

    def image_path(self, obj):
        return obj.image.path


admin.site.register(models.Gallery, GalleryAdmin)
