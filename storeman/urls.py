from django.contrib import admin
from django.urls import path
from .views import (
    admin_home,
    export_csv,
    export_pdf,
)
from .product_man import (
    product_list,
    create_product,
    display_product_detail,
    edit_product,
    delete_product,
)
from .address_man import (
    create_customer_address,
    edit_customer_address,
    delete_customer_address,
)
from .customer_man import (
    display_customer_list,
    display_customer_details,
    create_customer,
    edit_customer,
    delete_customer,
)

from .order_man import (
    order_list,
    create_order,
    order_details,
    submit_order,
)

from .staff_man import (
    display_staff,
)

app_name = "storeman"

urlpatterns = [
    path("", admin_home, name="admin_home"),
    path("order_list/", order_list, name="order_list"),
    path("create_order/", create_order, name="create_order"),
    path("order_details/<str:tk_no>", order_details, name="order_details"),
    path("export_csv/<str:tk_no>", export_csv, name="export_csv"),
    path("export_pdf/<str:tk_no>", export_pdf, name="export_pdf"),
    path("display_customer_list/", display_customer_list, name="display_customer_list"),
    path(
        "display_customer_details/<str:pk_id>",
        display_customer_details,
        name="display_customer_details",
    ),
    path(
        "create_customer_address/<str:pk_id>",
        create_customer_address,
        name="create_customer_address",
    ),
    path(
        "edit_customer_address/<str:pk_id>/<str:addr_id>",
        edit_customer_address,
        name="edit_customer_address",
    ),
    path(
        "delete_customer_address/<str:pk_id>/<str:addr_id>",
        delete_customer_address,
        name="delete_customer_address",
    ),
    path("create_customer/", create_customer, name="create_customer"),
    path("edit_customer/<str:pk_id>", edit_customer, name="edit_customer"),
    path("delete_customer/<str:pk_id>", delete_customer, name="delete_customer"),
    path("submit_order/", submit_order, name="submit_order"),
    # Product
    path("create_product/", create_product, name="create_product"),
    path("product_list/", product_list, name="product_list"),
    path(
        "display_product_detail/<str:pk_id>",
        display_product_detail,
        name="display_product_detail",
    ),
    path("edit_product/<str:pk_id>", edit_product, name="edit_product"),
    path("delete_product/<str:pk_id>", delete_product, name="delete_product"),
    # Staff
    path("display_staff/", display_staff, name="display_staff"),
]
