from rest_framework import serializers

from core.serializers.base import BaseSerializer
from .models import Type, Category, Tag, Product, Coupon


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(BaseSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(BaseSerializer):
    type = TypeSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = "__all__"


class CouponSerializer(BaseSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponListSerializer(BaseSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
