from django.shortcuts import render
from .filters import ProductFilter
from .models import Product


def product_index(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, "shop/product_index.html", {"filter": f})
