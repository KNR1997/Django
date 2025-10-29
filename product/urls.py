from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views.category import CategoryViewSet
from product.views.coupon import CouponViewSet
from product.views.product import ProductViewSet
from product.views.tag import TagViewSet
from product.views.type import TypeViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(
        "types/",
        TypeViewSet.as_view({"get": "list", "post": "create"}),
        name="type",
    ),
    path(
        "types/<uuid:pk>",
        TypeViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="type",
    ),
    path(
        "categories/",
        CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="category",
    ),
    path(
        "categories/<int:pk>",
        CategoryViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="category",
    ),
    path(
        "tags/",
        TagViewSet.as_view({"get": "list", "post": "create"}),
        name="tag",
    ),
    path(
        "tags/<int:pk>",
        TagViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="tag",
    ),
    path(
        "products/",
        ProductViewSet.as_view({"get": "list", "post": "create"}),
        name="product",
    ),
    path(
        "products/<int:pk>",
        ProductViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="product",
    ),
    path(
        "coupons/",
        CouponViewSet.as_view({"get": "list", "post": "create"}),
        name="coupon",
    ),
    path(
        "coupons/<int:pk>",
        CouponViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="coupon",
    )

]
