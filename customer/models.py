from django.db import models

from accounts.models import User
from core.models.base import BaseModel


# Create your models here.
# class Customer(BaseModel):
#     user = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = "Customer"
#         verbose_name_plural = "Customers"
#         db_table = "customers"
#
#     def __str__(self):
#         return f"Customer({self.user.display_name or self.user.email})"


class Address(BaseModel):
    ADDRESS_TYPE_CHOICES = (
        ("billing", "Billing"),
        ("shipping", "Shipping"),
    )
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    # metadata
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES)
    default = models.BooleanField(default=False)

    # address fields
    zip = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)

    # optional GPS location
    location = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "addresses"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} ({self.type}) - {self.street_address}, {self.city}"

    def save(self, *args, **kwargs):
        # ensure only one default per type per customer
        if self.default:
            Address.objects.filter(
                customer=self.customer, type=self.type
            ).update(default=False)
        super().save(*args, **kwargs)
