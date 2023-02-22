from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# Send Order cancel Email

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


@login_required(login_url="account_login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {"orders": orders}
    return render(request, "myinfo/myorders.html", context)


@login_required(login_url="account_login")
def order_view(request, tk_no):
    order = Order.objects.filter(tracking_no=tk_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {
        "order": order,
        "orderitems": orderitems,
    }
    return render(request, "myinfo/order_details.html", context)


@login_required(login_url="account_login")
def order_cancel(request, tk_no):
    order = Order.objects.get(tracking_no=tk_no, status="Pending")
    order.barcode_img.close()
    order.ami_file.close()
    order.ami_daily_file.close()
    order.order_pdf.close()
    order.barcode_img.delete()
    order.ami_file.delete()
    order.ami_daily_file.delete()
    order.order_pdf.delete()
    order.delete()

    template = render_to_string(
        "store/email_order_cancel.html",
        {"name": request.user, "tk_number": tk_no},
    )
    email = EmailMessage(
        f"[취소]고맙스온라인주문: {request.user}님의 주문이 취소되었습니다..",
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )

    email.fail_silently = False
    email.send()
    return redirect("store:myorders")
