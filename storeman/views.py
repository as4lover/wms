import base64
from django.contrib.auth.decorators import login_required

# from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Order, OrderItem
from django.contrib import messages

from .filters import ProductFilter

from customer.models import User
from company.models import AddressBook
from store.models import Product, OrderCode

# Import Pagination Stuff
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import csv
import codecs
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import pandas as pd
import os


# from store.utils import xhtml_render_to_pdf, weasypdf_render_to_pdf


@login_required(login_url="account_login")
def admin_home(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    orders = Order.objects.all().order_by("-created_at")
    pending_order = orders.filter(status="Pending").count()
    on_delivery = orders.filter(status="Out for delivery").count()
    delivered = orders.filter(status="Delivered").count()

    page_num = request.GET.get("page", 1)
    paginator = Paginator(orders, 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    page_num_counter = "a" * page_obj.paginator.num_pages

    context = {
        "orders": orders,
        "pending_order": pending_order,
        "on_delivery": on_delivery,
        "delivered": delivered,
        "page_obj": page_obj,
        "page_num_counter": page_num_counter,
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
