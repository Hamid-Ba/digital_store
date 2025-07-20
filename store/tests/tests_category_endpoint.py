from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from store import models

CATEGORY_URL = reverse("store:category-list")


def create_category(title, logo, order=1):
    """create category helper function"""
    return models.Category.objects.create(title=title, logo=logo, order=order)


class PublicTest(TestCase):
    """Brand Public Test"""

    def setUp(self) -> None:
        client = APIClient()
        return super().setUp()

    def test_list_of_category(self):
        """Test List Of Category"""
        create_category("category_1", "category_1.png")
        create_category("category_2", "category_2.png")

        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        category_count = models.Category.objects.count()
        self.assertEqual(len(res.data), category_count)
