from django.urls import path, include
from rest_framework.routers import DefaultRouter

from siteinfo import views

app_name = "site_info"

router = DefaultRouter()
router.register("faq", views.FAQViewSet)
router.register("faq_category", views.FAQCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("about_us/", views.AboutUsView.as_view(), name="about_us"),
    path("contact_us/", views.ContactUsView.as_view(), name="contact_us"),
    path("home_header/", views.HomeHeaderView.as_view(), name="home_header"),
    path("footer/", views.FooterView.as_view(), name="footer"),
    path(
        "slider_and_banner/",
        views.SliderAndBannerView.as_view(),
        name="slider_and_banner",
    ),
    path("ticket/", views.CreateTicketAPI.as_view(), name="create_ticket"),
    path("email_phone/", views.EmailAndPhoneAPI.as_view(), name="email_phone"),
]
