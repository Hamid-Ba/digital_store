from django.contrib import admin
from django import forms
from store import models
from django.utils import timezone
from django.utils.translation import activate, gettext_lazy as _

from jalali_date.admin import (
    ModelAdminJalaliMixin,
)

# from store.views import generate_pdf_invoice


class SubCategoryInline(admin.StackedInline):
    model = models.Category
    extra = 0
    verbose_name_plural = "Sub Categories"


class AddCategoryForm(forms.ModelForm):
    class Meta:
        models = models.Category

    def clean(self):
        is_cart = self.cleaned_data.get("is_cart")

        if is_cart:
            if models.Category.objects.filter(is_cart=True).count() < 4:
                return self.cleaned_data
            else:
                self.add_error(
                    "is_cart", "تعداد دسته بندی های کارتی بیشتر از ۴ مورد مجاز نمی باشد"
                )
                raise forms.ValidationError(
                    "تعداد دسته بندی های کارتی بیشتر از ۴ مورد مجاز نمی باشد"
                )


class CategoryAdmin(admin.ModelAdmin):
    form = AddCategoryForm
    list_display = ("title", "order", "parent")
    list_filter = ("parent",)
    search_fields = ("title",)

    inlines = [SubCategoryInline]

    fieldsets = (
        (None, {"fields": ("title", "logo", "order", "is_cart")}),
        (
            "Parent",
            {
                "fields": ("parent",),
                "description": "Select a category to make it a parent category",
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("sub_categories")

        return queryset


class SpecificationInline(admin.TabularInline):
    model = models.Specifications
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "is_active", "created_at")
    list_display_links = ("id", "full_name")
    list_editable = ("is_active",)


class GalleryInline(admin.TabularInline):
    model = models.Product.gallery.through


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "brand",
        "price",
        "count",
        "order_count",
    )
    list_display_links = ("id", "title")
    list_filter = ("category", "brand")
    list_editable = ["count"]
    search_fields = ("title", "category__title", "brand__title")
    filter_horizontal = ("gallery",)
    inlines = [SpecificationInline]

    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": ("title", "slug", "image", "short_desc", "desc"),
    #         },
    #     ),
    #     (
    #         "Image Details",
    #         {
    #             "fields": ("image_alt", "image_title"),
    #             "classes": ("collapse",),
    #         },
    #     ),
    #     (
    #         "Date",
    #         {
    #             "fields": ("publish_date",),
    #         },
    #     ),
    #     (
    #         "Tag and Category",
    #         {
    #             "fields": ("tags", "category"),
    #         },
    #     ),
    # )

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.prefetch_related("specs")

    #     return queryset


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = (
        "product_id",
        "brand",
        "title",
        "count",
    )
    extra = 1


class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
        "code",
        "state",
        "total_price",
        "user",
        "phone",
        "registered_date",
    )

    def registered_date(self, obj):
        activate("fa")  # Activate Persian language
        return timezone.localtime(obj.registered_date).strftime("%Y-%m-%d %H:%M:%S")

    registered_date.short_description = _("Persian Created At")
    # list_editable = ["registered_date"]
    # actions = ["generate_pdf_invoice"]
    inlines = [
        OrderItemInline,
    ]
    search_fields = ["code", "phone"]

    # def generate_pdf_invoice(self, request, queryset):
    #     for order in queryset:
    #         # Call the view to generate PDF for each selected order
    #         response = generate_pdf_invoice(request, order.id)
    #         return response

    # generate_pdf_invoice.short_description = "Generate PDF Invoice"


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "brand",
        "title",
        "price",
        "count",
        # "image_url",
    )


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price")
    list_display_links = ("id", "title")


admin.site.register(models.FavoriteProduct)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.PaymentMethod, PaymentMethodAdmin)
