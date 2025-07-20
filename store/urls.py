from rest_framework.routers import DefaultRouter
from django.urls import path, include

from store import views

app_name = "store"

router = DefaultRouter()
router.register("order", views.OrderViewSet)
router.register("products", views.ProductViewSet)
router.register("categories", views.CategoryViewSet)
router.register("payment_method", views.PaymentMethodViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "best_selling_products",
        views.BestSellingProductsAPI.as_view(),
        name="best_selling_products",
    ),
    path("search_products", views.SearchProductsAPI.as_view(), name="search_products"),
    path("all_categories", views.CategoryApiView.as_view(), name="all_categories"),
    # path("display_categories", views.DisplayCategoryApiView.as_view(), name="display_categories"),
    # path(
    #     "comment/<int:product_id>",
    #     views.ProductsCommentsApi.as_view(),
    #     name="product_comments",
    # ),
    path("place_order", views.CreateOrderApiView.as_view(), name="place_order"),
    path("comment", views.CreateCommentApi.as_view(), name="create_comment"),
    path(
        "favorite-products/",
        views.FavoriteProductListCreateView.as_view(),
        name="favorite-product-list-create",
    ),
]
