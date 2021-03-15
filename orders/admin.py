from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    fields = ("stripe_id",)


admin.site.register(Order, OrderAdmin)
