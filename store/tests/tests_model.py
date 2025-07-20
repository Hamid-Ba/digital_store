from django.test import TestCase

from store import models


class CategoryTest(TestCase):
    """Category Model Test"""

    def test_category_model(self):
        """Test Category Model"""
        payload = {"title": "test_category", "logo": "test.png", "order": 1}

        the_model = models.Category.objects.create(**payload)

        for key, value in payload.items():
            self.assertEqual(getattr(the_model, key), value)
