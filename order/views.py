from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from order.models import Order
from order.serializers import OrderListSerializer, OrderSerializer


# Create your views here.
class OrderViewSet(BaseViewSet):
    model = Order
    serializer_class = OrderListSerializer
    search_fields = ["name", "slug"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(
                super()
                .get_queryset()
                .prefetch_related("items", "items__product")
            )
        )

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderListSerializer(order).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
