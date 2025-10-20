from django.urls import path

from customer.views import CustomerViewSet

urlpatterns = [
    path(
        "customers/",
        CustomerViewSet.as_view({"get": "list", "post": "create"}),
        name="customer",
    ),
    path(
        "customers/<uuid:pk>",
        CustomerViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="customer",
    ),
]
