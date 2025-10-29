from django.db import models

from core.models.base import BaseModel


# Create your models here.
class Type(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    icon = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    translated_languages = models.JSONField(default=list)
    settings = models.JSONField(null=True, blank=True)
    banners = models.JSONField(default=list, null=True, blank=True)
    promotional_sliders = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        db_table = "type"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20)
    details = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=20)
    image = models.JSONField(null=True, blank=True)
    translated_languages = models.JSONField(default=list, blank=True)

    # ForeignKey to Type (many categories can belong to one type)
    type = models.ForeignKey(
        Type,
        related_name="categories",  # changed to 'categories' (more intuitive than 'types')
        on_delete=models.CASCADE
    )

    # Self-referential relationship (a category can have a parent category)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    icon = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    # ForeignKey to Type (a tag belongs to one Type)
    type = models.ForeignKey(
        Type,
        related_name="tags",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.name


# --- Enum-like choices for status and product_type ---
class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class ProductType(models.TextChoices):
    SIMPLE = "simple", "Simple"
    VARIABLE = "variable", "Variable"
    DIGITAL = "digital", "Digital"


class Product(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        null=True,
        blank=True,
        db_index=True
    )
    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        null=True,
        blank=True,
        db_index=True
    )
    price = models.FloatField()
    sale_price = models.FloatField()
    sku = models.IntegerField()
    unit = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    image = models.JSONField(null=True, blank=True)
    gallery = models.JSONField(default=list, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    # --- Relationships ---
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    type = models.ForeignKey(Type, related_name="products", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name


class CouponType(models.TextChoices):
    FIXED = "fixed", "Fixed"
    PERCENTAGE = "percentage", "Percentage"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=20)
    description = models.TextField(null=True)
    type = models.CharField(max_length=20, choices=CouponType.choices, db_index=True)
    amount = models.FloatField()
    minimum_cart_amount = models.FloatField()
    active_from = models.DateTimeField()
    expire_at = models.DateTimeField()
    is_valid = models.BooleanField(default=False)
    # target = models.IntegerField()
    translated_languages = models.JSONField(default=list)

    class Meta:
        db_table = "coupon"

    def __str__(self):
        return self.code
