from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from store.models import Order, OrderItem
from django.contrib import messages
from django_tables2 import RequestConfig
from .forms import OrderForm
from storeman.tables import OrderListTable
from .filters import OrderListFilter

import os, pathlib, glob
import datetime
import pandas as pd
import mimetypes


@login_required(login_url="account_login")
def order_list(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    orders = Order.objects.all().order_by("-created_at")
    table = OrderListTable(orders)
    RequestConfig(request, paginate={"per_page": 5}).configure(table)
    context = {
        "table": table,
    }
    return render(request, "storeman/order/order_list.html", context)


def daily_order(request):
    daily_order = Order.objects.filter(status="Pending")
    daily_count = daily_order.count()
    media_filepath = pathlib.Path(settings.MEDIA_ROOT)
    order_filepath = pathlib.Path(media_filepath, "order")
    daily_filepath = pathlib.Path(order_filepath, "daily")
    os.chdir(daily_filepath)
    csv_files = glob.glob(f"ami-*.csv")
    csv_files_count = len(csv_files)
    merged_file = glob.glob(f"daily*.csv")
    context = {
        "daily_oder": daily_order,
        "daily_count": daily_count,
        "csv_files": csv_files,
        "csv_files_count": csv_files_count,
        "merged_files": merged_file,
    }
    return render(request, "storeman/order/daily_order.html", context)


@login_required(login_url="account_login")
def submit_order(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    daily_order = Order.objects.filter(status="Pending")
    media_filepath = pathlib.Path(settings.MEDIA_ROOT)
    order_filepath = pathlib.Path(media_filepath, "order")
    daily_filepath = pathlib.Path(order_filepath, "daily")
    os.chdir(daily_filepath)
    now = datetime.datetime.now()
    csv_files = glob.glob(f"ami-*.csv")
    merged_file = glob.glob(f"daily*.csv")
    if merged_file == []:
        daily_merge_name = (
            f"daily_ami_merged-{now.year}{now.month}{now.day}{now.hour}{now.minute}.csv"
        )
        df_append = pd.concat(map(pd.read_csv, csv_files))
        df_append.to_csv(daily_merge_name, encoding="utf-8", index=False, header=False)
        daily_order.update(status="Out for delivery")
        messages.info(request, "알맹이용 파일이 만들어졌습니다.")
    else:
        print(merged_file)
        messages.info(request, "알맹이용파일이 있습니다.")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


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
