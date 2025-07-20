from django.test import TestCase
from django.contrib.auth import get_user_model

from province import models as province_model
from address import models

# Create your tests here.


def create_user(phone, password):
    """Helper Function for creating a user"""
    return get_user_model().objects.create_user(phone=phone, password=password)


def create_province(province):
    return province_model.Province.objects.create(name=province, slug=province)


def create_city(city, province_id):
    return province_model.City.objects.create(
        name=city, slug=city, province=province_id
    )


class AddressModel(TestCase):
    """Address Model Test"""

    def test_address_model(self):
        """Test Address Model"""
        user = create_user("09151498721", "123456")
        province = create_province("tehran")
        city = create_city("tehran", province)

        payload = {
            "desc": "Test Address",
            "street": "Test Street",
            "postal_code": "12345",
            "user": user,
            "province": province,
            "city": city,
        }
        the_model = models.Address.objects.create(**payload)

        for k, v in payload.items():
            self.assertEqual(getattr(the_model, k), v)

        self.assertEqual(the_model.user, user)
        self.assertEqual(the_model.city, city)
        self.assertEqual(the_model.province, province)
