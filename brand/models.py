import os
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


def brand_logo_file_path(instance, filename):
    """Generate file path for brand logo"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "banner", filename)


class Brand(models.Model):
    """Brand Model"""

    title = models.CharField(max_length=72, verbose_name="عنوان")
    logo = models.ImageField(
        null=False, upload_to=brand_logo_file_path, verbose_name="لوگو"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("برند")
        verbose_name_plural = _("برندها")
