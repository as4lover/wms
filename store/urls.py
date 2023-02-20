from django.contrib import admin
from django.urls import path, include
from . import views, cart, checkout, order

app_name = "store"

urlpatterns = [
    # path("", views.home, name="home"),
    path("", cart.wishlist_view, name="home"),
    # path("", views.category, name="home"),
    path("category/", views.category, name="category"),
    path("product/<str:slug>", views.product_list, name="product_list"),
    path(
        "product/<str:cat_slug>/<str:prd_id>",
        views.product_detail,
        name="product_detail",
    ),
    # 제품검색
    # path("search", views.search_ajax),
    # path("searchproducts", views.searchproducts, name="searchproducts"),
    path("search/", views.search, name="search"),
    # Cart
    path("add-to-cart", cart.addtocart, name="addtocart"),
    path("cart", cart.viewcart, name="cart"),
    path("update-cart", cart.updatecart, name="updatecart"),
    path("delete-cart-item", cart.deletecartitem, name="deletecartitem"),
    # 주문
    path("checkout", checkout.index, name="checkout"),
    path("place-order", checkout.place_order, name="place_order"),
    # 주문상세내역
    path("my-orders", order.my_orders, name="myorders"),
    path("order-view/<str:tk_no>", order.order_view, name="orderview"),
    path("my-orders/<str:tk_no>", order.order_cancel, name="order_cancel"),
    # path("export_csv/<str:tk_no>", order.export_csv, name="export_csv"),
    # path("export_pdf/<str:tk_no>", order.export_pdf, name="export_pdf"),
    # 자주주문내역
    path("wish_list", cart.wishlist_view, name="wishlist_view"),
    path("add_to_wishlist", cart.add_to_wishlist, name="add_to_wishlist"),
    path("delete_wish_item", cart.delete_wishitem, name="delete_wishitem"),
    path("add_wish_to_cart", cart.add_wish_to_cart, name="add_wish_to_cart"),
    # Language code
    # path('/language/<str:language_code>', views.set_language, name='set_language'),
]
