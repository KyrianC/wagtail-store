from cart.forms import CartAddProductForm

from django.db import models
from django.db.models import Func, F
from django.utils.html import format_html

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(Page):
    category = models.ForeignKey(
        "shop.Category", related_name="products", on_delete=models.SET_NULL, null=True
    )
    thumbnail = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("description"),
        FieldPanel("price"),
        ImageChooserPanel("thumbnail"),
        FieldPanel("available"),
    ]

    # Return uppercase bold name for ModelAdmin list
    def name(self):
        return format_html("<strong>{}</strong>", self.title.upper())

    def get_recommendations(self):
        """
        Get recommendation based on similar price in the same category
        """
        RECOMMENDATION_NUMBER = 3
        return (
            Product.objects.filter(category=self.category)
            .annotate(price_diff=Func(F("price") - self.price, function="abs"))
            .exclude(id=self.id)
            .order_by("price_diff")[:RECOMMENDATION_NUMBER]
        )

    def get_context(self, request):
        context = super().get_context(request)
        recommendations = self.get_recommendations()
        cart_form = CartAddProductForm()
        context["cart_form"] = cart_form
        context["recommendations"] = recommendations
        return context


class ProductList(Page):
    def get_context(self, request):
        context = super().get_context(request)
        products = self.get_children().live().order_by("-first_published_at")
        context["products"] = products
        return context
