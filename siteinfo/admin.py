"""
site info module admin models
"""
from django.contrib import admin

from siteinfo import models


class AboutUsAdmin(admin.ModelAdmin):
    """About Us Admin Model"""

    list_display = ["id", "title"]
    list_display_links = ["id", "title"]

    fieldsets = (
        (
            "Main Info",
            {
                "classes": ("collapse",),
                "fields": ("title", "text"),
            },
        ),
    )


class ContactUsAdmin(admin.ModelAdmin):
    """Contact Us Admin Model"""

    list_display = ["id", "title"]
    list_display_links = ["id", "title"]

    fieldsets = (
        (
            "Main Info",
            {
                "classes": ("collapse",),
                "fields": ("title", "text"),
            },
        ),
    )


class HomeHeaderAdmin(admin.ModelAdmin):
    """Home Header Admin Model"""

    list_display = ["id", "heading", "is_active"]
    list_display_links = ["id", "heading"]
    list_editable = ["is_active"]


class FooterAdmin(admin.ModelAdmin):
    """Footer Admin Model"""

    list_display = ["id", "heading", "is_active"]
    list_display_links = ["id", "heading"]
    list_editable = ["is_active"]


class SliderAndBannerAdmin(admin.ModelAdmin):
    """Contact Us Admin Model"""

    list_display = ["id", "heading", "is_slider"]
    list_display_links = ["id", "heading"]
    list_editable = ["is_slider"]


class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    list_display_links = (
        "id",
        "title",
    )


class FAQAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "category",
    )
    list_display_links = (
        "id",
        "question",
    )
    list_filter = ("category",)


class EmailAndPhoneAdmin(admin.ModelAdmin):
    list_display = ("email1", "email2", "phone1", "phone2")
    list_display_links = ("email1", "email2", "phone1", "phone2")
    list_editable = ("email1", "email2", "phone1", "phone2")


admin.site.register(models.Ticket)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.register(models.Footer, FooterAdmin)
admin.site.register(models.AboutUs, AboutUsAdmin)
admin.site.register(models.ContactUs, ContactUsAdmin)
admin.site.register(models.HomeHeader, HomeHeaderAdmin)
admin.site.register(models.FAQCategory, FAQCategoryAdmin)
admin.site.register(models.SliderAndBanner, SliderAndBannerAdmin)
