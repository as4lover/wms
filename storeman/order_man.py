from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from store.models import Order, OrderItem
from django.contrib import messages
from .forms import OrderForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url="account_login")
def submit_order(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    orders = Order.objects.filter(status="Pending")
    print(orders.count())
    ami_file_name = []
    if orders.count() != 0:
        for order in orders:
            print(order.tracking_no)
        orders.update(status="Out for delivery")
    else:
        messages.info(request, "주문이 없습니다.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="account_login")
def order_list(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    orders = Order.objects.all()
    # Set up Pagination
    page_num = request.GET.get("page", 1)
    paginator = Paginator(orders, 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    page_num_counter = "a" * page_obj.paginator.num_pages
    context = {"page_obj": page_obj, "page_num_counter": page_num_counter}
    return render(request, "storeman/order_list.html", context)


@login_required(login_url="account_login")
def order_details(request, tk_no):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    order = Order.objects.filter(tracking_no=tk_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {"order": order, "orderitems": orderitems}
    return render(request, "storeman/order_details.html", context)


@login_required(login_url="account_login")
def create_order(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    formset = OrderFormSet()
    content = {"formset": formset}
    return render(request, "storeman/create_order.html", content)
