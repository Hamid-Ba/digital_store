"""
site info module models
"""

from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class AboutUs(models.Model):
    """About Us Model"""

    title = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="عنوان"
    )
    text = RichTextField(blank=True, null=True, verbose_name="متن")

    class Meta:
        verbose_name = _("درباره ما")
        verbose_name_plural = _("درباره ما")


class ContactUs(models.Model):
    """Contact Us Model"""

    title = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="عنوان"
    )
    text = RichTextField(blank=True, null=True, verbose_name="متن")

    class Meta:
        verbose_name = _("تماس با ما")
        verbose_name_plural = _("تماس با ما")


class Ticket(models.Model):
    """Ticket Model"""

    full_name = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="نام کامل"
    )
    phone = models.CharField(
        max_length=11, null=False, blank=False, verbose_name="موبایل"
    )
    text = models.CharField(max_length=500, null=False, blank=False, verbose_name="متن")
    create_data = models.DateTimeField(auto_now_add=True, verbose_name="زمان ارسال")

    def __str__(self) -> str:
        return f"{self.full_name} - {self.phone}"

    class Meta:
        verbose_name = _("تیکت")
        verbose_name_plural = _("تیکت ها")


class HomeHeader(models.Model):
    """Home Header"""

    header = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
        verbose_name="لینک تیتر",
    )

    heading = models.CharField(
        max_length=72, null=True, blank=True, verbose_name="سر تیتر"
    )
    paragraph = models.CharField(
        max_length=300, null=True, blank=True, verbose_name="توضیح تیتر"
    )
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = _("تیتر صفحه اصلی")
        verbose_name_plural = _("تیتر صفحه اصلی")


class Footer(models.Model):
    """Footer"""

    heading = models.CharField(
        max_length=72, null=True, blank=True, verbose_name="تیتر"
    )
    paragraph = models.CharField(
        max_length=300, null=True, blank=True, verbose_name="پاراگراف"
    )

    # instagram = models.URLField(
    #     max_length=250,
    #     blank=True,
    #     null=True,
    #     error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    # )

    # tweeter = models.URLField(
    #     max_length=250,
    #     blank=True,
    #     null=True,
    #     error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    # )

    # telegram = models.URLField(
    #     max_length=250,
    #     blank=True,
    #     null=True,
    #     error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    # )

    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = _("فوتر")
        verbose_name_plural = _("فوتر")


class SliderAndBanner(models.Model):
    """Banner"""

    image = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
        verbose_name="تصویر",
    )

    heading = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="تیتر"
    )
    paragraph = models.CharField(
        max_length=125, null=True, blank=True, verbose_name="پاراگراف"
    )
    link_text = models.CharField(
        max_length=72, null=True, blank=True, verbose_name="متن لینک"
    )

    link_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
        verbose_name="آدرس لینک",
    )

    is_slider = models.BooleanField(default=False, verbose_name="آیا اسلایدر هست ؟")

    class Meta:
        verbose_name = _("اسلایدر و بنر")
        verbose_name_plural = _("اسلایدر و بنرها")


class FAQCategory(models.Model):
    title = models.CharField(max_length=125, verbose_name="دسته بندی")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("دسته سوالات")
        verbose_name_plural = _("دسته های سوالات")


class FAQ(models.Model):
    category = models.ForeignKey(
        FAQCategory, on_delete=models.CASCADE, related_name="faqs", verbose_name="دسته"
    )
    question = models.CharField(max_length=500, verbose_name="سوال")
    answer = RichTextField(verbose_name="جواب")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("سوال")
        verbose_name_plural = _("سوالات")


class EmailAndPhone(models.Model):
    email1 = models.EmailField(null=True, blank=True, verbose_name="پست الکترونیک اول")
    email2 = models.EmailField(null=True, blank=True, verbose_name="پست الکترونیک دوم")
    phone1 = models.CharField(
        max_length=17, null=True, blank=True, verbose_name="شماره تماس اول"
    )
    phone2 = models.CharField(
        max_length=17, null=True, blank=True, verbose_name="شماره تماس دوم"
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("نشانی")
        verbose_name_plural = _("نشانی ها")
