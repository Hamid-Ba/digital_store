import os
from uuid import uuid4
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common import validators
from brand import models as brand_models
from gallery import models as gallery_models
from address import models as address_models

from discount import models as discount_models

# Create your models here.


def category_logo_file_path(instance, filename):
    """Generate file path for category image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "category", filename)


class CategoryManager(models.Manager):
    """Category Manager"""

    def get_parents_category(self):
        """return main category"""
        return self.filter(parent=None).order_by("order")


class Category(models.Model):
    """Category Model"""

    title = models.CharField(
        max_length=72, null=False, blank=False, verbose_name="عنوان"
    )
    logo = models.ImageField(
        null=True, blank=True, upload_to=category_logo_file_path, verbose_name="لوگو"
    )
    order = models.IntegerField(default=1, verbose_name="الویت نمایش")
    is_cart = models.BooleanField(default=False, verbose_name="نمایش به صورت کارتی ؟")

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_categories",
        verbose_name="دسته پدر",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("دسته محصولات")
        verbose_name_plural = _("دسته های محصولات")

    objects = CategoryManager()


class ProductManager(models.Manager):
    """Product Manager"""

    def get_relational_products_by_category(self, product_id, cat_id):
        """return products in same category"""
        return (
            self.filter(category=cat_id)
            .exclude(id=product_id)
            .order_by("-order_count")
            .all()[:8]
        )


class Product(BaseModel):
    """Product Model"""

    title = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="عنوان"
    )
    price = MoneyField(
        max_digits=12,
        decimal_places=0,
        default_currency="IRR",
        null=False,
        verbose_name="قیمت",
    )
    short_desc = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="توضیحات کوتاه"
    )
    desc = RichTextField(blank=True, null=True, verbose_name="توضیحات")
    # technical_number = models.CharField(max_length=125, null=True, blank=True, verbose_name="کد فنی")
    count = models.IntegerField(default=0, verbose_name="موجودی انبار")
    order_count = models.IntegerField(default=0, verbose_name="تعداد سفارش")
    # weight = models.FloatField(default=0, verbose_name="وزن (کیلو گرم)")
    # created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_contacted = models.BooleanField(
        default=False, verbose_name="آیا تماس گرفته شود؟"
    )
    limit_count = models.IntegerField(default=0, verbose_name="محدودیت در تعداد سفارش")

    gallery = models.ManyToManyField(
        gallery_models.Gallery, related_name="products", verbose_name="گالری"
    )

    brand = models.ForeignKey(
        brand_models.Brand,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="برند",
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="دسته"
    )

    def __str__(self):
        return self.title

    def can_order(self, count):
        return count < self.count

    def ordered(self, count):
        self.order_count += count
        self.count -= count
        self.save()

    def get_active_comments(self):
        return self.comments.filter(is_active=True).order_by("created_at").values()

    objects = ProductManager()

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")


class Specifications(models.Model):
    """Specifications Model"""

    key = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="مشخصه"
    )
    value = models.CharField(
        max_length=225, null=False, blank=False, verbose_name="مقدار"
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specs", verbose_name="محصول"
    )

    def __str__(self):
        return f"{self.product.title}-{self.key}"

    class Meta:
        verbose_name = _("مشخصه محصول")
        verbose_name_plural = _("مشخصات محصولات")


class Comment(BaseModel):
    """Commnet Model"""

    full_name = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="نام کامل"
    )
    text = models.CharField(max_length=750, null=False, blank=False, verbose_name="متن")
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments", verbose_name="محصول"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="کاربر",
    )

    def __str__(self) -> str:
        return f"{self.full_name} commented for {self.product.title}"

    class Meta:
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")


class PaymentMethod(models.Model):
    """Payment Method Model"""

    title = models.CharField(
        max_length=125, null=False, blank=False, verbose_name="عنوان"
    )
    price = MoneyField(
        max_digits=10,
        decimal_places=0,
        default_currency="IRR",
        null=False,
        verbose_name="هزینه",
    )
    price_per_kilo = MoneyField(
        max_digits=10,
        decimal_places=0,
        default_currency="IRR",
        null=True,
        blank=True,
        verbose_name="قیمت هر کیلوگرم",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("روش پرداخت")
        verbose_name_plural = _("روش های پرداخت")


class Order(models.Model):
    class OrderState(models.TextChoices):
        PENDING = "P", "در انتظار بررسی (پرداخت شده)"
        CONFIRMED = "D", "تکمیل شده"
        REJECTED = "C", "لغو شده / پر داخت ناموفق"
        DOING = "DD", "در دست اقدام"

    code = models.CharField(
        max_length=225, blank=False, null=True, verbose_name="کد سفارش"
    )
    state = models.CharField(
        max_length=2,
        default=OrderState.PENDING,
        choices=OrderState.choices,
        verbose_name="وضعیت",
    )
    total_price = MoneyField(
        max_digits=10,
        decimal_places=0,
        default_currency="IRR",
        null=False,
        verbose_name="قیمت کل",
    )
    phone = models.CharField(
        max_length=11,
        blank=False,
        null=False,
        validators=[validators.PhoneValidator],
        verbose_name="موبایل",
    )
    registered_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="تاریخ ثبت سفارش"
    )
    address = models.ForeignKey(
        address_models.Address,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        verbose_name="نشانی",
    )

    confirmed_date = models.DateTimeField(
        null=True, blank=True, editable=True, verbose_name="تاریخ تکمیل شده"
    )
    rejected_date = models.DateTimeField(
        null=True, blank=True, editable=True, verbose_name="تاریخ لغو شده"
    )
    doing_date = models.DateTimeField(
        null=True, blank=True, editable=True, verbose_name="تاریخ در دست اقدام"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کاربر",
    )

    discount = models.ForeignKey(
        discount_models.DiscountCode,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        verbose_name="تخفیف",
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name="روش پرداخت",
    )

    def __str__(self):
        return f"Order #{self.id}-{self.code}"

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش ها")


class OrderItem(models.Model):
    product_id = models.BigIntegerField(
        null=True, blank=True, verbose_name="شناسه محصول"
    )
    brand = models.CharField(max_length=125, null=True, blank=True, verbose_name="برند")
    title = models.CharField(
        max_length=125, null=True, blank=True, verbose_name="عنوان"
    )
    # image_url = models.CharField(max_length=250, null=False, blank=False)
    price = MoneyField(
        max_digits=10,
        decimal_places=0,
        default_currency="IRR",
        null=True,
        verbose_name="قیمت",
    )
    # technical_number = models.CharField(max_length=125, null=True, blank=True, verbose_name="کد فنی")
    count = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="تعداد")

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="سفارش"
    )

    def __str__(self):
        return f"Order #{self.product_id}-{self.title}"

    class Meta:
        verbose_name = _("آیتم سفارش")
        verbose_name_plural = _("آیتم های سفارش")


class FavoriteProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_products",
        verbose_name="کاربر",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="محصول",
    )

    def __str__(self) -> str:
        return f"{self.product.title}-{self.product.technical_number}"

    class Meta:
        unique_together = ("user", "product")
        verbose_name = _("مورد علاقه")
        verbose_name_plural = _("مورد علاقه ها")
