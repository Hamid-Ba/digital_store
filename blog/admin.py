from django.contrib import admin
from blog import models
from jalali_date.admin import (
    ModelAdminJalaliMixin,
)


class SubCategoryInline(admin.StackedInline):
    model = models.BlogCategory
    extra = 0
    verbose_name_plural = "Sub Categories"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "sub_category")
    list_filter = ("sub_category",)
    search_fields = ("title",)

    inlines = [SubCategoryInline]

    fieldsets = (
        (None, {"fields": ("title", "image", "order")}),
        (
            "Image Details",
            {
                "fields": ("image_alt", "image_title"),
                "classes": ("collapse",),
            },
        ),
        (
            "Sub Category",
            {
                "fields": ("sub_category",),
                "description": "Select a category to make it a parent category",
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("sub_categories")

        return queryset


# class SpecificationInline(admin.TabularInline):
#     model = models.Specification
#     extra = 1


class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("title", "category", "publish_date")
    list_filter = ("category", "tags")
    search_fields = ("title", "short_desc", "desc")

    # inlines = [SpecificationInline]

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug", "image", "short_desc", "desc"),
            },
        ),
        (
            "Image Details",
            {
                "fields": ("image_alt", "image_title"),
                "classes": ("collapse",),
            },
        ),
        (
            "Date",
            {
                "fields": ("publish_date",),
            },
        ),
        (
            "Tag and Category",
            {
                "fields": ("tags", "category"),
            },
        ),
    )

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.prefetch_related("specs")

    #     return queryset


# class SpecificationAdmin(admin.ModelAdmin):
#     list_display = ("key", "type", "value", "blog")
#     list_filter = ("type",)
#     search_fields = ("key", "value", "blog__title")


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.BlogCategory, CategoryAdmin)
# admin.site.register(models.Specification, SpecificationAdmin)
