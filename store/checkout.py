from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
import weasyprint
from .models import Cart, Order, OrderItem, Product
from company.models import AddressBook

import random
import datetime
import math

import csv, os, platform
from io import StringIO, BytesIO
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
import weasyprint

from django.core.files import File
import barcode
from barcode.writer import ImageWriter

# Send email
from django.core.mail import EmailMessage
from django.conf import settings


@login_required(login_url="account_login")
def index(request):
    company = AddressBook.objects.get(user=request.user, default=True)
    # raw_cart = Cart.objects.filter(user=request.user)
    # for item in raw_cart:
    #     if item.product_qty > item.product.quantity:
    #         Cart.objects.delete(id=item.id)
    cart_items = Cart.objects.filter(user=request.user)
    # total_price = 0
    # for item in cart_items:
    #     total_price = total_price + item.product.sale_price * item.product_qty

    context = {
        "cart_items": cart_items,
        # "total_price": total_price,
        "company": company,
    }
    return render(request, "store/checkout.html", context)


@login_required(login_url="account_login")
def place_order(request):
    company = AddressBook.objects.get(user=request.user, default=True)
    new_order = Order()
    new_order.user = request.user
    new_order.company_name = company.h_name
    new_order.company_e_name = company.e_name
    new_order.fname = company.user.first_name
    new_order.lname = company.user.last_name
    new_order.phone = company.user.phone
    new_order.email = company.user.email
    new_order.address = company.address
    new_order.city = company.city
    new_order.state = company.state
    new_order.postcode = company.postcode
    new_order.representative = company.representative.name
    new_order.rep_first_name = company.representative.name.first_name
    new_order.rep_last_name = company.representative.name.last_name
    new_order.message = request.POST.get("message")

    cart = Cart.objects.filter(user=request.user)
    cart_total_price = 0
    for item in cart:
        cart_total_price = cart_total_price + item.product.sale_price * item.product_qty
    new_order.total_price = cart_total_price
    now_time = datetime.datetime.now()
    trk_date = now_time.strftime("%y%m%d")
    trackno = trk_date + str(random.randint(1111, 9999))
    while Order.objects.filter(tracking_no=trackno) is None:
        trackno = trk_date + str(random.randint(1111, 9999))
    new_order.tracking_no = trackno
    # Barcode
    EAN = barcode.get_barcode_class("code39")
    barcode_num = str(trackno)
    ean = EAN(barcode_num, writer=ImageWriter(), add_checksum=False)
    buffer = BytesIO()
    ean.write(buffer)
    new_order.barcode_img.save(f"{barcode_num}.png", File(buffer), save=False)
    new_order.save()
    # ======= 각 Order 아이템의 야채코드와 일반코드 추출하기
    new_order_items = Cart.objects.filter(user=request.user)
    order_code = AddressBook.objects.get(user__username=request.user, default=True)
    veg_code = order_code.vegi_code
    gen_code = order_code.gen_code

    for item in new_order_items:
        item_category = item.product.category.title
        if item_category == "야채":
            order_code = veg_code
            order_type = "야채"
        if item_category != "야채":
            order_code = gen_code
            order_type = "일반"
        OrderItem.objects.create(
            order=new_order,
            product=item.product,
            price=item.product.sale_price,
            quantity=item.product_qty,
            order_code=order_code,
            order_type=order_type,
        )
    # To decrease the product qty from available stock
    order_product = Product.objects.filter(id=item.product.id).first()
    # order_product.quantity = order_product.quantity - item.product_qty
    order_product.save()
    # To Clear user's Cart
    Cart.objects.filter(user=request.user).delete()
    # ============ 알맹이를 위한 CSV file 저장하기
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["주문일자", "주문업체코드", "주문업체명", "제품코드", "제품명", "수량"])
    order = Order.objects.filter(tracking_no=trackno).first()
    orderitems = OrderItem.objects.filter(order=order)
    for item in orderitems:
        if item.product.unit == "EA" and item.product.per_box != 1:
            # ===== 소수점2자리 무조건 올림하기
            item_each = item.quantity / item.product.per_box
            decimals = 2
            multiplier = 10**decimals
            item_quantity = math.ceil(item_each * multiplier) / multiplier
        else:
            # if item.product.unit == "CTN":
            item_quantity = item.quantity

        writer.writerow(
            [
                item.order.created_at.strftime("%Y-%m-%d"),
                item.order_code,
                item.order.company_name,
                item.product.bar_code,
                item.product.title,
                item_quantity,
            ]
        )
    csv_file = ContentFile(csv_buffer.getvalue().encode("utf-8-sig"))
    order.ami_file.save(f"ami-{trackno}.csv", csv_file)

    # PDF 주문서 작성
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
    order_code = item_code
    order_type = item_type
    # order_category = order.category
    message = order.message
    representative = order.representative
    rep_first_name = order.rep_first_name
    rep_last_name = order.rep_last_name
    context = {
        "orderitems": orderitems,
        "tk_no": trackno,
        "company_name": company_name,
        "company_e_name": company_e_name,
        "first_name": first_name,
        "last_name": last_name,
        "city": city,
        "phone": phone,
        "order_date": order_date,
        "order_code": order_code,
        "order_type": order_type,
        # "order_category": order_category,
        "message": message,
        "representative": representative,
        "rep_first_name": rep_first_name,
        "rep_last_name": rep_last_name,
    }
    html = render_to_string("storeman/pdf-output.html", context)
    out = BytesIO()
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(out)
    pdf_file = ContentFile(out.getvalue())
    order.order_pdf.save(f"{trackno}.pdf", pdf_file)

    # 주문완료 메일 보내기
    template = render_to_string(
        "store/email_order_completed.html",
        {
            "name": request.user,
            "tk_number": trackno,
            "company_e_name": company_e_name,
            "address": new_order.address,
        },
    )
    email = EmailMessage(
        f"고맙스온라인주문: {request.user}님의 주문이 완료되었습니다.",
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )

    email.fail_silently = False
    email.send()
    messages.success(request, "주문이완료되었습니다.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
