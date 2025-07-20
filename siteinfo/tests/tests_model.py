"""
Test site info module models
"""
from django.test import TestCase

from siteinfo.models import AboutUs, ContactUs


class AboutUsTest(TestCase):
    """Test About Us Model"""

    def test_create_aboutUs_model_should_work_properly(self):
        """Test Create About Us Model"""
        payload = {
            "title": "test",
            "text": "Lorem ipsum dolor sit amet, consectetur adip",
        }

        about_us = AboutUs.objects.create(**payload)

        for key, value in payload.items():
            self.assertEqual(getattr(about_us, key), value)


class ContactUsTest(TestCase):
    """Test Contact Us Model"""

    def test_create_contact_us_model_should_work_properly(self):
        """Test Create Contact Us Model"""
        payload = {
            "title": "test",
            "text": "Lorem ipsum dolor sit amet, consectetur adip",
        }

        contact_us = ContactUs.objects.create(**payload)

        for key, value in payload.items():
            self.assertEqual(getattr(contact_us, key), value)
