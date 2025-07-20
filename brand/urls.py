from django.urls import path
from brand import views

app_name = "brand"

urlpatterns = [path("brands", views.BrandsApiView.as_view(), name="brands")]
