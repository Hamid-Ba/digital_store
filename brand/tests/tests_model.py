from django.test import TestCase

from brand import models


class BrandTest(TestCase):
    """Brand Model"""

    def test_brand_model(self):
        payload = {"logo": "test.png", "title": "Test Name"}

        the_model = models.Brand.objects.create(**payload)
        the_model.save()

        for key, value in payload.items():
            self.assertEqual(getattr(the_model, key), value)
