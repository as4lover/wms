import base64
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Order, OrderItem
from delivery.models import StaffMember

from customer.models import User
from company.models import AddressBook
from store.models import Product, OrderCode
from .tools import *

# Import Pagination Stuff
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import csv
import codecs
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from datetime import datetime, date
import pandas as pd
import os, pytz


au_timezone = pytz.timezone("Australia/Sydney")
today = date.today()
now = datetime.now(au_timezone)
now_year = now.year
now_month = now.month
now_day = now.day
this_monday = get_this_monday()
this_friday = get_this_friday()
last_monday = get_last_monday()
last_friday = get_last_friday()
this_month_start = get_this_month_start()
this_month_end = get_this_month_end()
last_month_start = get_last_month_start()
last_month_end = get_last_month_end()
# from store.utils import xhtml_render_to_pdf, weasypdf_render_to_pdf


@login_required(login_url="account_login")
def admin_home(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    order_item = OrderItem.objects.filter(order__status="Delivered")
    staffs = StaffMember.objects.all()
    order_team = Order.objects.filter(
        updated_at__year=now_year,
        updated_at__month=now_month,
        updated_at__day=now_day,
    )
    drivers = []
    teams = []
    for driver in order_team:
        driver_id = driver.driver
        drivers.append(driver_id)
    for drv in drivers:
        staff = staffs.filter(name__username=drv)
        for team in staff:
            teams.append(team.region)
    east_team = teams.count("동부팀")
    west_team = teams.count("서부팀")
    south_team = teams.count("남부팀")
    north_team = teams.count("북부팀")
    pending_order = Order.objects.filter(status="Pending").count()
    on_delivery = Order.objects.filter(status="Out for delivery").count()
    delivered = Order.objects.filter(
        status="Delivered",
        updated_at__year=now_year,
        updated_at__month=now_month,
        updated_at__day=now_day,
    ).count()
    this_weekly_delivered = Order.objects.filter(
        status="Delivered", updated_at__range=[this_monday, this_friday]
    ).count()

    last_weekly_delivered = Order.objects.filter(
        status="Delivered", updated_at__range=[last_monday, last_friday]
    ).count()

    this_monthly_delivered = Order.objects.filter(
        status="Delivered", updated_at__range=[this_month_start, this_month_end]
    ).count()

    last_monthly_delivered = Order.objects.filter(
        status="Delivered", updated_at__range=[last_month_start, last_month_end]
    ).count()

    yearly_delivered = Order.objects.filter(
        status="Delivered", updated_at__year=now_year
    ).count()

    print(east_team)
    print(west_team)
    print(south_team)
    print(north_team)
    context = {
        "east_team": east_team,
        "west_team": west_team,
        "south_team": south_team,
        "north_team": north_team,
        "order_item": order_item,
        "pending_order": pending_order,
        "on_delivery": on_delivery,
        "delivered": delivered,
        "this_weekly_delivered": this_weekly_delivered,
        "last_weekly_delivered": last_weekly_delivered,
        "this_monthly_delivered": this_monthly_delivered,
        "last_monthly_delivered": last_monthly_delivered,
        "yearly_delivered": yearly_delivered,
    }
    return render(request, "storeman/dashboard.html", context)


@login_required(login_url="account_login")
def export_csv(request, tk_no):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment;filename=ami" + f"-{tk_no}.csv"
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(["주문일자", "주문업체코드", "주문업체명", "제품코드", "제품명", "수량"])
    order = Order.objects.filter(tracking_no=tk_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    for item in orderitems:
        writer.writerow(
            [
                item.order.created_at.strftime("%Y-%m-%d"),
                item.order.user.number,
                item.order.user.company_name,
                item.product.bar_code,
                item.product.title,
                item.quantity,
            ]
        )
    return response


@login_required(login_url="account_login")
def export_pdf(request, tk_no):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    with open("media/order/barcode/" + f"{tk_no}.png", "rb") as img:
        encoded_string = base64.b64decode(img.read())
    response = HttpResponse(content_type="application/pdf")
    # 화면에 먼저 보여주기 inline; 추가
    response["Content-Disposition"] = "inline; attachment;filename=" + f"{tk_no}.pdf"
    response["Content-Transfer-Encoding"] = "binary"
    order = Order.objects.filter(tracking_no=tk_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    # delivery_method = OrderCode.objects.get(code=order.order_code)
    for item in orderitems:
        item_code = item.order_code
        item_type = item.order_type
    company_name = order.company_name
    company_e_name = order.company_e_name
    first_name = order.user.first_name
    last_name = order.user.last_name
    phone = order.user.phone
    city = order.city
    order_date = order.created_at
    # order_category = orderitems.product.category
    # order_code = item_code
    order_type = item_type
    total_price = order.total_price
    message = order.message

    # delivery_instructions = delivery_method.delivery_instructions
    html_string = render_to_string(
        "storeman/pdf-output.html",
        {
            "orderitems": orderitems,
            "tk_no": tk_no,
            "company_name": company_name,
            "company_e_name": company_e_name,
            "first_name": first_name,
            "last_name": last_name,
            "city": city,
            "phone": phone,
            "order_date": order_date,
            # "order_code": order_code,
            "order_type": order_type,
            "total_price": total_price,
            # "order_category": order_category,
            "message": message,
        },
    )

    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response
