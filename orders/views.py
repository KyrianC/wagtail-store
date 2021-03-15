from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm, OrderRetrieveForm
from .tasks import order_created
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            # order_created.delay(order.id)
            print(
                request.build_absolute_uri(
                    order.items.first()
                    .product.thumbnail.get_rendition("height-200")
                    .url
                )
            )
            return render(request, "orders/created.html", {"order_id": order.id})
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"cart": cart, "form": form})

def order_retrieve(request):
    order = None
    if request.method == 'POST':
        form = OrderRetrieveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.filter(id=cd['id']).first()
    else:
        form = OrderRetrieveForm()
    return render(request, "orders/retrieve.html", {"form": form, "order": order})