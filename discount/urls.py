from rest_framework.routers import DefaultRouter
from django.urls import path, include

from discount import views

app_name = "discount"

urlpatterns = [
    path("get_code/<str:code>", views.DiscountCodeApiView.as_view(), name="get_code")
]
