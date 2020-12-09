from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("create/<int:order_id>/", views.create_payment, name="create"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path("hook/", views.my_webhook_view, name="hook"),
]
