from django.db import models

from accounts.models import User
from core.models.base import BaseModel
from product.models import Product


# Create your models here.
class Order(BaseModel):
    PAYMENT_GATEWAYS = [
        ("CASH_ON_DELIVERY", "Cash on Delivery"),
        ("CARD", "Card"),
        ("PAYPAL", "PayPal"),
        ("OTHER", "Other"),
    ]

    ORDER_STATUSES = [
        ("order-pending", "Order Pending"),
        ("order-processing", "Order Processing"),
        ("order-completed", "Order Completed"),
        ("order-cancelled", "Order Cancelled"),
    ]

    PAYMENT_STATUSES = [
        ("payment-pending", "Payment Pending"),
        ("payment-completed", "Payment Completed"),
        ("payment-failed", "Payment Failed"),
        ("payment-refunded", "Payment Refunded"),
    ]

    tracking_number = models.CharField(max_length=30, unique=True)
    # ForeignKey to User (many order can belong to one user)
    customer = models.ForeignKey(
        User,
        related_name="orders",  # changed to 'categories' (more intuitive than 'types')
        on_delete=models.CASCADE
    )
    customer_contact = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sales_tax = models.DecimalField(max_digits=10, decimal_places=2)
    paid_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    note = models.TextField(blank=True, null=True)

    cancelled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cancelled_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cancelled_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_gateway = models.CharField(max_length=50, choices=PAYMENT_GATEWAYS)
    altered_payment_gateway = models.CharField(max_length=50, null=True, blank=True)
    logistics_provider = models.CharField(max_length=100, null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_time = models.CharField(max_length=100, null=True, blank=True)

    order_status = models.CharField(max_length=50, choices=ORDER_STATUSES)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUSES)

    wallet_point = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "order"

    def __str__(self):
        return f"Order #{self.tracking_number} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    name = models.CharField(max_length=255)  # Increased length for long product names
    sku = models.CharField(max_length=100, null=True, blank=True)  # SKU may not always be numeric
    unit = models.CharField(max_length=50)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    # Optional fields (good for tracking)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    class Meta:
        db_table = "order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def save(self, *args, **kwargs):
        """Auto-calculate subtotal before saving."""
        price_to_use = self.sale_price if self.sale_price else self.price
        self.subtotal = price_to_use * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (x{self.quantity})"
