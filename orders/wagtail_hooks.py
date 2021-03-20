from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin

from treemodeladmin.options import TreeModelAdmin

from .models import Order, OrderItem, Refund


class OrderItemModelAdmin(TreeModelAdmin):
    model = OrderItem
    parent_field = "order"
    list_display = (
        "product",
        "quantity",
        "get_cost",
    )
    list_filter = ("product",)
    search_fields = ("product",)


@modeladmin_register
class OrderModelAdmin(TreeModelAdmin):
    menu_label = "Orders"
    menu_icon = "list-ul"
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    # add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    # exclude_from_explorer = False
    model = Order
    inspect_view_enabled = True
    child_field = "items"
    child_model_admin = OrderItemModelAdmin
    list_display = ("id", "paid", "status", "get_total_cost")
    list_filter = ("paid", "status")
    list_export = ("updated",)
    search_fields = ("email", "first_name", "last_name", "city", "State", "stripe_id")


@modeladmin_register
class RefundModelAdmin(ModelAdmin):
    model = Refund
    menu_label = "Refunds"
    menu_icon = "placeholder"
    menu_order = 300
    inspect_view_enabled = True
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False
    list_display = ("order", "status", "created", "updated")
