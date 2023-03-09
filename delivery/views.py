from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from store.models import *
from .forms import OrderForm, ItemStatusForm
from .table import MyDeliveryTable, MyDeliveryDetailTable
from django_tables2 import RequestConfig


@login_required(login_url="account_login")
def delivery_home(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    orders = Order.objects.filter(
        driver=request.user, status="Pending"
    ) | Order.objects.filter(driver=request.user, status="Out for delivery")
    context = {"orders": orders}
    return render(request, "delivery/delivery_home.html", context)


@login_required(login_url="account_login")
def delivery_details(request, tk_no):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    order = Order.objects.filter(tracking_no=tk_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    form = OrderForm(instance=order)  # update를 위해 instance 사용
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
        return redirect(request.META["HTTP_REFERER"])
    else:
        context = {
            "order": order,
            "orderitems": orderitems,
            "form": form,
        }
    return render(request, "delivery/delivery_details.html", context)


def delivery_items_status(request, pk_id):
    orderitems = OrderItem.objects.get(id=pk_id)
    item_form = ItemStatusForm(instance=orderitems)  # update를 위해 instance 사용
    if request.method == "POST":
        item_form = ItemStatusForm(request.POST, instance=orderitems)
        if item_form.is_valid():
            item_form.save()
    context = {
        "item_form": item_form,
        "orderitems": orderitems,
    }
    return render(request, "delivery/delivery_items_status.html", context)


def my_delivery_list(request, user):
    order_list = Order.objects.filter(driver=user, status="Delivered").order_by(
        "-updated_at"
    )
    order_items = OrderItem.objects.filter(order=order_list)
    my_table = MyDeliveryTable(order_list)
    RequestConfig(request, paginate={"per_page": 5}).configure(my_table)
    context = {"my_table": my_table}
    return render(request, "delivery/my_delivery_list.html", context)


def my_delivery_detail(request, pk_id):
    order_details = Order.objects.filter(id=pk_id).first()
    orderitems = OrderItem.objects.filter(order=order_details)
    item_table = MyDeliveryDetailTable(orderitems)
    context = {"order_details": order_details, "item_table": item_table}
    return render(request, "delivery/my_delivery_detail.html", context)


def vegi_order_list(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    vegi_order = OrderItem.objects.filter(order_type="야채")
    context = {"vegi_order": vegi_order}
    return render(request, "delivery/vegi_order_list.html", context)
