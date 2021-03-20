import uuid
from django.db import models
from shop.models import Product


# DONE change id to uuid, so we can show order's uuid to customers for them to retrieve past orders
class Order(models.Model):
    INCOMPLETE = "ac"
    AWAITING_PAYMENT = "ap"
    AWAITING_FULLFILEMENT = "p"
    CANCELLED = "c"
    FULLFILED = "f"
    STATUS_CHOICES = [
        (INCOMPLETE, "Awaiting Checkout"),
        (AWAITING_PAYMENT, "Awaiting Payment"),
        (AWAITING_FULLFILEMENT, "Awaiting Fullfilement"),
        (CANCELLED, "Cancelled"),
        (FULLFILED, "Fullfiled"),
    ]
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#uuidfield
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default=INCOMPLETE)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # TODO send different emails in each cases through tasks
    def update_status_paid(self):
        self.status = self.AWAITING_FULLFILEMENT
        self.paid = True
        self.save()

    def update_status_cancelled(self):
        self.status = self.CANCELLED
        self.save()

    def update_status_awaiting_payment(self):
        self.status = self.AWAITING_PAYMENT
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_product(self):
        return self.product.title


class Refund(models.Model):
    AWAITING = "d"
    REFUSED = "x"
    PROCESSING = "p"
    REFUNDED = "rf"
    STATUS_CHOICES = [
        (AWAITING, "Awaiting decision"),
        (REFUSED, "Refund Declined"),
        (PROCESSING, "Processing Refund"),
        (REFUNDED, "Successfully Refunded"),
    ]
    message = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=AWAITING)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"refund for order {self.order}"


class RefundImage(models.Model):
    image = models.ImageField()
    refund = models.ForeignKey(Refund, related_name="images", on_delete=models.CASCADE)
