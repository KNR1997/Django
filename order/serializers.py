from rest_framework import serializers

from core.serializers.base import BaseSerializer
from order.models import Order, OrderItem


class OrderItemSerializer(BaseSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'name', 'sku', 'price', 'sale_price', 'quantity', 'unit')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        # Create related order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


# class OrderSerializer(serializers.ModelSerializer):
#     # items = OrderItemSerializer(many=True, write_only=True)
#
#     class Meta:
#         model = Order
#         fields = [
#             'tracking_number',
#             'customer_id',
#             # 'customer_contact',
#             # 'customer_name',
#             # 'amount',
#             # 'sales_tax',
#             # 'paid_total',
#             # 'total',
#             # 'note',
#             # 'payment_gateway',
#             # 'delivery_fee',
#             # 'delivery_time',
#             # 'order_status',
#             # 'payment_status',
#             # 'items'
#         ]
#
#     def create(self, validated_data):
#         items_data = validated_data.pop('items', [])
#         order = Order.objects.create(**validated_data)
#
#         # Create related order items
#         for item_data in items_data:
#             OrderItem.objects.create(order=order, **item_data)
#
#         # Optionally update totals
#         total_amount = sum(
#             (item_data.get('sale_price') or item_data.get('price')) * item_data.get('quantity')
#             for item_data in items_data
#         )
#         order.amount = total_amount
#         order.total = total_amount + order.delivery_fee + order.sales_tax
#         order.paid_total = order.total
#         order.save()
#
#         return order


class OrderListSerializer(BaseSerializer):
    items = OrderItemSerializer(many=True, allow_null=True)

    class Meta:
        model = Order
        fields = ('id', 'tracking_number', 'amount', 'items', 'created_by', 'created_at')


class OrderItemLiteSerializer(BaseSerializer):
    class Meta:
        model = OrderItem
        fields = ['name', 'sku', 'price', 'sale_price', 'quantity']
        read_only_fields = fields
