from django.urls import path
from .views import (
    delivery_home,
    delivery_details,
    delivery_items_status,
    vegi_order_list,
)

app_name = "delivery"

urlpatterns = [
    path("", delivery_home, name="delivery_home"),
    path("delivery_details/<str:tk_no>", delivery_details, name="delivery_details"),
    path(
        "delivery_items_status/<str:pk_id>",
        delivery_items_status,
        name="delivery_items_status",
    ),
    path("vegi_order", vegi_order_list, name="vegi_order_list"),
]
