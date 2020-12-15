import django_filters
from django.forms import CheckboxSelectMultiple
from django_filters import (
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    OrderingFilter,
    RangeFilter,
)

from .models import Category, Product


class ProductFilter(django_filters.FilterSet):
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "filter-checkbox"}),
    )
    price = RangeFilter()
    sort = OrderingFilter(
        field_name="Sort by",
        fields=[
            ("price", "Price"),
        ],
    )

    class Meta:
        model = Product
        fields = ("category", "price")
