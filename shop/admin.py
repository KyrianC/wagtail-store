from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin

from .models import Product

# Register your models here.
class ProductAdmin(ThumbnailMixin, ModelAdmin):
    model = Product
    menu_label = "products"
    menu_icon = "placeholder"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False
    list_display = ("admin_thumb", "name", "category", "price")
    list_filter = ("category", "live")
    list_export = ("title", "category", "price")
    thumb_image_field_name = "thumbnail"

    # Optionally override the filter spec used to create each thumb
    thumb_image_filter_spec = "fill-100x100"  # this is the default

    # Optionally override the 'width' attribute value added to each `<img>` tag
    thumb_image_width = 50  # this is the default

    # Optionally override the class name added to each `<img>` tag
    thumb_classname = "admin-thumb"  # this is the default

    # Optionally override the text that appears in the column header
    thumb_col_header_text = "image"  # this is the default

    # Optionally specify a fallback image to be used when the object doesn't
    # have an image set, or the image has been deleted. It can an image from
    # your static files folder, or an external URL.
    # thumb_default = 'https://lorempixel.com/100/100'


modeladmin_register(ProductAdmin)
