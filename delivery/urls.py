from django.urls import path
from .views import delivery_home, delivery_details, vegi_order_list

app_name = "delivery"

urlpatterns = [
    path("", delivery_home, name="delivery_home"),
    path("delivery_details/<str:tk_no>", delivery_details, name="delivery_details"),
    path("vegi_order", vegi_order_list, name="vegi_order_list"),
]
