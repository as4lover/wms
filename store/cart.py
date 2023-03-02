from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from .models import Cart, Product, WishItem
from company.models import AddressBook


@login_required(login_url="account_login")
def addtocart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get("product_id"))
        product_check = Product.objects.get(id=prod_id)
        print(prod_id)
        if product_check:
            if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                return JsonResponse({"status": "주문서에 이미 있습니다."})
            else:
                prod_qty = int(request.POST.get("product_qty"))
                if product_check.quantity >= prod_qty:
                    Cart.objects.create(
                        user=request.user,
                        product_id=prod_id,
                        product_qty=prod_qty,
                    )
                    return JsonResponse({"status": "주문서에 추가했습니다."})
                else:
                    return JsonResponse(
                        {"status": "현재 재고가 " + str(product_check.quantity) + "개 있습니다."}
                    )
        else:
            return JsonResponse({"status": "주문서에 제품이 없습니다."})
    else:
        return JsonResponse({"status": "로그인 해주세요"})
    return redirect("/")


@login_required(login_url="account_login")
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    address = AddressBook.objects.filter(user=request.user)
    context = {"cart": cart, "address": address}
    return render(request, "store/cart.html", context)


@login_required(login_url="account_login")
def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get("product_id"))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            prod_qty = int(request.POST.get("product_qty"))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({"status": "수량이 변경되었습니다."})
    return redirect("/")


@login_required(login_url="account_login")
def deletecartitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get("product_id"))
        if Cart.objects.filter(
            user=request.user,
            product_id=prod_id,
        ):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({"status": "주문내용을 지웠습니다 "})
    return redirect("/")


# 자주주문제품들
@login_required(login_url="account_login")
def wishlist_view(request):
    if request.user.is_staff and request.user.role == "MANAGER":
        return redirect("/delivery")
    if request.user.is_staff and request.user.role == "DRIVER":
        return redirect("/delivery")
    if request.user.is_staff and request.user.role == "ADMIN":
        return redirect("/storeman")
    else:
        wish_items = WishItem.objects.filter(user=request.user)
        if wish_items.count() == 0:
            return redirect("store:category")
        else:
            context = {
                "wish_items": wish_items,
            }
        return render(request, "store/wishlist.html", context)


@login_required(login_url="account_login")
def add_to_wishlist(request):
    if request.method == "POST":
        prod_id = int(request.POST.get("product_id"))
        product_check = Product.objects.get(id=prod_id)
        if product_check:
            if WishItem.objects.filter(user=request.user.id, product_id=prod_id):
                return JsonResponse({"status": "제품이 이미 있습니다."})
            else:
                WishItem.objects.create(
                    user=request.user,
                    product_id=prod_id,
                )
                output = _("Add to Favorites")
                return JsonResponse({"status": output})
        else:
            return JsonResponse({"status": "제품이 없습니다."})


@login_required(login_url="account_login")
def delete_wishitem(request):
    if request.method == "POST":
        prod_id = int(request.POST.get("product_id"))
        if WishItem.objects.filter(user=request.user, product_id=prod_id):
            wish_item = WishItem.objects.get(user=request.user, product_id=prod_id)
            wish_item.delete()
        return JsonResponse({"status": "제품리스트에서 지웠습니다."})
    return redirect("/")


@login_required(login_url="account_login")
def add_wish_to_cart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get("product_id"))
        product_check = Product.objects.get(id=prod_id)
        if product_check:
            if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                return JsonResponse({"status": "제품이 이미 있습니다."})
            else:
                prod_qty = 1
                Cart.objects.create(
                    user=request.user, product_id=prod_id, product_qty=prod_qty
                )
                return JsonResponse({"status": _("Add to Order list")})
    else:
        return JsonResponse({"status": "로그인 해주세요"})
    return redirect("/")
