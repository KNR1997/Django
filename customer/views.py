from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from accounts.models import User
from core.views.base import BaseViewSet
from customer.serializers import CustomerListSerializer, CustomerSerializer


# Create your views here.
class CustomerViewSet(BaseViewSet):
    model = User
    serializer_class = CustomerListSerializer
    search_fields = ["name", "slug"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        try:
            serializer = CustomerSerializer(
                data={**request.data}
            )
            if serializer.is_valid():
                serializer.save()

                user = User.objects.filter(email=serializer.data["email"]).first()

                serializer = CustomerListSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"name": "A customer is already exits"},
                    status=status.HTTP_409_CONFLICT,
                )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
