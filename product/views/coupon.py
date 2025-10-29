from core.permissions.base import allow_permission, ROLE
from core.views.base import BaseViewSet
from product.models import Type, Coupon
from product.serializers import CouponSerializer


# Create your views here.
class CouponViewSet(BaseViewSet):
    model = Coupon
    serializer_class = CouponSerializer
    search_fields = ["code"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN], creator=True, model=Type)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN], creator=True, model=Type)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
