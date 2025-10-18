from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from product.models import Tag
from product.serializers import TagListSerializer, TagSerializer


# Create your views here.
class TagViewSet(BaseViewSet):
    model = Tag
    serializer_class = TagListSerializer
    search_fields = ["name", "slug"]
    filterset_fields = ["type__id"]

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related("type"))
        )

    def create(self, request):
        try:
            serializer = TagSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"slug": "The tag with the slug already exists"},
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
