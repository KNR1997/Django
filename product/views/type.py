from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from product.models import Type
from product.serializers import TypeSerializer


# Create your views here.
class TypeViewSet(BaseViewSet):
    model = Type
    serializer_class = TypeSerializer
    search_fields = ["name", "slug"]
    filterset_fields = ["type__id"]

    def get_queryset(self):
        # Add your prefetch/select optimizations
        return (
            super()
            .get_queryset()
            .select_related("type")
            .prefetch_related("categories", "tags")
        )

    def list(self, request, *args, **kwargs):
        # Get filtered queryset
        queryset = self.get_queryset()

        # Apply pagination if set in settings.py
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not enabled
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        type = (
            self.get_queryset()
            .filter(pk=pk)
        ).first()

        if type is None:
            return Response(
                {"error": "Type does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(Type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = TypeSerializer(
            data={**request.data}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk, *args, **kwargs):
        type = Type.objects.get(pk=pk)
        serializer = TypeSerializer(
            type,
            data={**request.data},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        type = Type.objects.get(pk=pk)
        type.delete()
