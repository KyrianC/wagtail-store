import stripe
from django.conf import settings  # new
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.views.decorators.csrf import csrf_exempt  # new
from django.views.decorators.http import require_POST
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def success(request):
    return render(request, "payment/success.html")


def cancel(request):
    return render(request, "payment/cancel.html")


@csrf_exempt
def create_payment(request, order_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = get_object_or_404(Order, id=order_id)
    item_list = []
    for item in order.items.all():
        item_list.append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": f"{item.price*100:.0f}",
                    "product_data": {
                        "name": item.product.title,
                        "images": [
                            request.build_absolute_uri(
                                item.product.thumbnail.get_rendition("height-200").url
                            )
                        ],
                    },
                },
                "quantity": item.quantity,
            },
        )
    session = stripe.checkout.Session.create(
        customer_email=order.email,
        payment_method_types=["card"],
        line_items=item_list,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment:success")),
        cancel_url=request.build_absolute_uri(reverse("payment:cancel")),
    )
    order.stripe_id = session["id"]
    order.save()
    return JsonResponse({"id": session["id"]})


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Save an order in your database, marked as 'awaiting payment'
        order = Order.objects.get(stripe_id=session["id"])
        order.update_status_awaiting_payment()

        # Check if the order is already paid (e.g., from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            order.update_status_paid()

    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]

        # Fulfill the purchase
        order.update_status_paid()

    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]

        # Send an email to the customer asking them to retry their order
        order.update_status_cancelled()

    # Passed signature verification
    return HttpResponse(status=200)
