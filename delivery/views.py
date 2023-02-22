from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from store.models import *
from .forms import OrderForm


@login_required(login_url="account_login")
def delivery_home(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    orders = Order.objects.filter(
        representative=request.user, status="Pending"
    ) | Order.objects.filter(representative=request.user, status="Out for delivery")
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
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    context = {
        "order": order,
        "orderitems": orderitems,
        "form": form,
    }
    return render(request, "delivery/delivery_details.html", context)


def vegi_order_list(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    vegi_order = OrderItem.objects.filter(order_type="야채")
    context = {"vegi_order": vegi_order}
    return render(request, "delivery/vegi_order_list.html", context)
