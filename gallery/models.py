import os
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

# Create your models here.


def gallery_image_file_path(instance, filename):
    """Generate file path for category image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "gallery", filename)


class Gallery(models.Model):
    """Gallery model"""

    title = models.CharField(
        max_length=125, blank=True, null=True, verbose_name="عنوان"
    )
    image = models.ImageField(
        null=False, upload_to=gallery_image_file_path, verbose_name="تصویر"
    )

    def __str__(self):
        if self.title:
            return self.title
        return self.image

    class Meta:
        verbose_name = _("گالری")
        verbose_name_plural = _("گالری")
