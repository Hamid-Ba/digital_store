"""
Test Gallery Module Models
"""
from django.test import TestCase

from gallery import models


class GalleryTest(TestCase):
    """Test Gallery Model"""

    def test_create_gallery_model_should_work_properly(self):
        """Test Create Gallery Model"""
        gallery = {"title": "New Pic", "image": "no_image.jpg"}

        created_gallery = models.Gallery.objects.create(**gallery)

        for key, value in gallery.items():
            self.assertEqual(getattr(created_gallery, key), value)

        self.assertEqual(created_gallery.title, gallery["title"])
