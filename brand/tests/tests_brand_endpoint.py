from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from brand import models

BRAND_URL = reverse("brand:brands")


def create_brand(title, logo):
    """create brand helper function"""
    return models.Brand.objects.create(title=title, logo=logo)


class PublicTest(TestCase):
    """Brand Public Test"""

    def setUp(self) -> None:
        client = APIClient()
        return super().setUp()

    def test_list_of_brand(self):
        """Test List Of Brand"""
        create_brand("brand_1", "brand_1.png")
        create_brand("brand_2", "brand_2.png")

        res = self.client.get(BRAND_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        brands_count = models.Brand.objects.count()
        self.assertEqual(len(res.data), brands_count)
