from django.db import models
from shop.models import Product


# TODO add an uuid field to show customers and help them retrieve their orders


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

    # TODO send different emails in each cases
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
