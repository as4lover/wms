from django.urls import path
from .views import (
    delivery_home,
    delivery_details,
    delivery_items_status,
    my_delivery_list,
    my_delivery_detail,
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
    path("my_delivery_list/<str:user>", my_delivery_list, name="my_delivery_list"),
    path(
        "my_delivery_detail/<str:pk_id>", my_delivery_detail, name="my_delivery_detail"
    ),
    path("vegi_order", vegi_order_list, name="vegi_order_list"),
]
