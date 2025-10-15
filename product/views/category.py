from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from product.models import Category
from product.serializers import CategoryListSerializer, CategorySerializer


# Create your views here.
class CategoryViewSet(BaseViewSet):
    model = Category
    serializer_class = CategoryListSerializer
    search_fields = ["name", "slug"]
    filterset_fields = ["type__id"]

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related("type"))
        )

    def create(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            type = request.data.get("type", False)

            if not type:
                return Response(
                    {"error": "Both name and slug are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"slug": "The category with the slug already exists"},
                    status=status.HTTP_409_CONFLICT,
                )


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
