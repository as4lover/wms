from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.base import File
from store.models import Order, OrderItem, DailyJobs
from django.contrib import messages
from django_tables2 import RequestConfig
from .forms import OrderForm
from storeman.tables import OrderListTable, dailyOrderTable
from .filters import OrderListFilter

import os, pathlib, glob
from PyPDF3 import PdfFileMerger
import datetime
import pandas as pd


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


@login_required(login_url="account_login")
def daily_order(request):
    daily_order = Order.objects.filter(status="Pending")
    daily_merged = DailyJobs.objects.all().order_by("-created_at")
    daily_table = dailyOrderTable(daily_merged)
    RequestConfig(request, paginate={"per_page": 5}).configure(daily_table)
    daily_count = daily_order.count()
    media_filepath = pathlib.Path(settings.MEDIA_ROOT)
    order_filepath = pathlib.Path(media_filepath, "order")
    daily_filepath = pathlib.Path(order_filepath, "daily")
    os.chdir(daily_filepath)
    csv_files = glob.glob(f"ami-*.csv")
    pdf_files = glob.glob(f"*.pdf")
    csv_files_count = len(csv_files)
    pdf_files_count = len(pdf_files)
    merged_csv_file = glob.glob(f"daily*.csv")
    merged_pdf_file = glob.glob(f"daily*.pdf")
    merged_files = merged_csv_file + merged_pdf_file
    context = {
        "daily_table": daily_table,
        "daily_oder": daily_order,
        "daily_count": daily_count,
        "csv_files": csv_files,
        "csv_files_count": csv_files_count,
        "pdf_files_count": pdf_files_count,
        "merged_files": merged_files,
        "daily_merged": daily_merged,
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
    print(len(csv_files))
    if len(csv_files) == 0:
        messages.info(request, "CSV 파일들이 없습니다...")
    else:
        daily_temp = "temp.csv"
        daily_merge_name = (
            f"daily_ami_merged-{now.year}{now.month}{now.day}{now.hour}{now.minute}.csv"
        )
        df_append = pd.concat(map(pd.read_csv, csv_files))
        df_append.to_csv(
            daily_temp,
            encoding="utf-8",
            index=False,
        )
        temp_data = pd.read_csv(daily_temp, encoding="utf-8-sig")
        df = pd.DataFrame(temp_data)
        without_vegi_data = df[~df["제품코드"].str.contains("V")]
        without_vegi_data.to_csv(
            daily_merge_name, encoding="utf-8-sig", index=False
        )  # 야채오더 제외
        os.remove("temp.csv")
        # csv file database에 넣기
        save_daily_ami = DailyJobs.objects.create(created_user=request.user)
        save_daily_ami.daily_merged_csv.save(
            daily_merge_name, File(open(daily_merge_name, "r"))
        )
        ### 주문장 하나로 합치기
        pdf_files = glob.glob(f"*.pdf")
        merger = PdfFileMerger()
        for pdf in pdf_files:
            merger.append(pdf)
        merged_pdf = (
            f"daily_merged_pdf-{now.year}{now.month}{now.day}{now.hour}{now.minute}.pdf"
        )
        merger.write(merged_pdf)
        merger.close()
        # PDF file database에 넣기
        save_daily_ami.daily_merged_pdf.save(
            merged_pdf, File(open(merged_pdf, "rb"))
        )  # PDF는 바이트형식이라 반드시 rb로 읽어야함
        # daily 파일들 지우기
        for daily_order_list in daily_order:
            daily_order_list.ami_daily_file.close()
            daily_order_list.ami_daily_file.delete()
            daily_order_list.pdf_daily_file.close()
            daily_order_list.pdf_daily_file.delete()
        all_csv_files = glob.glob(f"*.csv")
        all_pdf_files = glob.glob(f"*.pdf")
        all_files = all_csv_files + all_pdf_files
        for files in all_files:
            try:
                os.remove(files)
            except OSError as e:
                print("Error")
        # DB Status update from Pending to Our for delivery
        daily_order.update(status="Out for delivery")
        messages.info(request, "알맹이용 파일이 만들어졌습니다.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="account_login")
def order_list_detail(request, pk_id):
    order_list = Order.objects.filter(id=pk_id).first()
    order_items = OrderItem.objects.filter(order=order_list)
    context = {"order_list": order_list, "order_items": order_items}
    return render(request, "storeman/order/order_list_detail.html", context)


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
