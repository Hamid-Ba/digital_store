from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)

from address import views

app_name = "address"

router = DefaultRouter()
router.register("address", views.AddressViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
