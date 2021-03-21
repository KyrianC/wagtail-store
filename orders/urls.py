from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="create"),
    path("retrieve/", views.order_retrieve, name="retrieve"),
    path("refund/<uuid:order_uuid>", views.order_refund_request, name="refund"),
]
