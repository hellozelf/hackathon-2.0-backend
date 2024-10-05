from django.db import models


class Author(models.Model):
    """
    TODO: When the data is being created or updated we don't know, need to add that information
    """
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=1024, db_index=True, unique=True)
    url = models.CharField(max_length=1024, blank=True, )
    title = models.CharField(max_length=1024, blank=True, )
    big_metadata = models.JSONField(blank=True, null=True)
    secret_value = models.JSONField(blank=True, null=True)
    followers = models.IntegerField(default=0)


class Content(models.Model):
    """
    TODO: When the data is being created or updated we don't know, need to add that information
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=1024, )
    url = models.CharField(max_length=1024, blank=True, )
    title = models.TextField(blank=True)
    like_count = models.BigIntegerField(blank=True, null=False, default=0, )
    comment_count = models.BigIntegerField(blank=True, null=False, default=0, )
    view_count = models.BigIntegerField(blank=True, null=False, default=0, )
    share_count = models.BigIntegerField(blank=True, null=False, default=0, )
    thumbnail_url = models.URLField(max_length=1024, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True, )
    big_metadata = models.JSONField(blank=True, null=True)
    secret_value = models.JSONField(blank=True, null=True)


class Tag(models.Model):
    """
    TODO: The tag is being duplicated sometimes, need to do something in the database.
    Filtering
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class ContentTag(models.Model):
    """
    TODO: The content and tag is being duplicated, need to do something in the database
    """
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class MegaEcommerce(models.Model):
    """
    TODO: Normalize the model
    """
    # User Information
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)  # Storing password hashes in the same table is a security risk
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)

    # Address Information (multiple addresses in one field)
    addresses = models.JSONField(default=list)  # List of dictionaries containing address details

    # Product Information
    product_id = models.IntegerField()  # Not unique, as it's repeated for each order
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.CharField(max_length=100)
    product_subcategory = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=100)
    product_stock = models.IntegerField()
    product_ratings = models.JSONField(default=list)  # List of dictionaries containing rating details

    # Order Information
    order_id = models.IntegerField()  # Not unique, as it's repeated for each product in the order
    order_date = models.DateTimeField()
    order_status = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    # Order Item Information
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Payment Information
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    # Supplier Information
    supplier_id = models.IntegerField()
    supplier_name = models.CharField(max_length=255)
    supplier_contact_name = models.CharField(max_length=255)
    supplier_email = models.EmailField()
    supplier_phone = models.CharField(max_length=20)

    # Inventory Information
    warehouse_id = models.IntegerField()
    warehouse_name = models.CharField(max_length=255)
    warehouse_location = models.CharField(max_length=255)
    shelf_number = models.CharField(max_length=50)
    reorder_point = models.IntegerField()

    # Customer Service Information
    support_ticket_id = models.IntegerField(null=True, blank=True)
    support_ticket_status = models.CharField(max_length=50, null=True, blank=True)
    support_agent_name = models.CharField(max_length=255, null=True, blank=True)

    # Marketing Campaign Information
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_name = models.CharField(max_length=255, null=True, blank=True)
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Wishlist Information
    wishlist_items = models.JSONField(default=list)  # List of product IDs

    # Review Information
    review_text = models.TextField(null=True, blank=True)
    review_rating = models.IntegerField(null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - Order {self.order_id} - Product {self.product_name}"

    class Meta:
        # This isn't a proper unique constraint, as it would prevent users from ordering the same product twice
        # It's just to illustrate the complexity of the denormalized model
        unique_together = ('user_id', 'order_id', 'product_id')
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['order_id']),
            models.Index(fields=['product_id']),
            models.Index(fields=['payment_id']),
        ]
