# from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *

# Import Pagination Stuff
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def set_language(request, language_code):
#     translation.activate(language_code)
#     request.session[translation.LANGUAGE_SESSION_KEY] = language_code
#     return HttpResponse(status=200)


@login_required(login_url="account_login")
def home(request):
    if request.user.is_superuser:
        return redirect("/storeman")
    if request.user.is_staff and request.user.role == "DRIVER":
        return redirect("/delivery")
    else:

        category = Category.objects.all()
        context = {"category": category, "next": next}
        return render(request, "store/home.html", context)


@login_required(login_url="account_login")
def category(request):
    category = Category.objects.all()
    context = {"category": category}
    return render(request, "store/category.html", context)


@login_required(login_url="account_login")
def product_list(request, slug):
    if Category.objects.filter(slug=slug):
        products = Product.objects.filter(category__slug=slug, is_active=True)
        category = Category.objects.filter(slug=slug).first()
        # Set up Pagination
        page_num = request.GET.get("page", 1)
        paginator = Paginator(products, 8)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        page_num_counter = "a" * page_obj.paginator.num_pages
        context = {
            "page_obj": page_obj,
            "page_num_counter": page_num_counter,
            "category": category,
        }
        return render(request, "store/product_list.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect("category")


@login_required(login_url="account_login")
def product_detail(request, cat_slug, prd_id):
    if Category.objects.filter(slug=cat_slug):
        if Product.objects.filter(id=prd_id, is_active=True):
            products = Product.objects.filter(id=prd_id, is_active=True).first()
            context = {"products": products}
        else:
            messages.error(request, "No such Category found")
            return redirect("category")
    else:
        messages.error(request, "No such Category found")
        return redirect("category")
    return render(request, "store/product_detail.html", context)


@login_required(login_url="account_login")
def search_ajax(request):
    h_products = Product.objects.filter(is_active=True).values_list("title", flat=True)
    e_products = Product.objects.filter(is_active=True).values_list(
        "e_title", flat=True
    )
    h_products_list = list(h_products)
    e_products_list = list(e_products)
    plus_product = h_products_list + e_products_list
    products_list = list(filter(None, plus_product))  # list 안에 빈 값지우기
    return JsonResponse(products_list, safe=False)


@login_required(login_url="account_login")
def searchproducts(request):
    if request.method == "POST":
        searchedterm = request.POST.get("productsearch")
        if searchedterm == "":
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            product = (
                Product.objects.filter(title__contains=searchedterm)
                | Product.objects.filter(e_title__icontains=searchedterm)
            ).first()
            if product:
                return redirect(
                    "product/" + product.category.slug + "/" + str(product.id)
                )
            else:
                messages.info(request, "찾는 제품이없습니다.")
                return redirect(request.META.get("HTTP_REFERER"))
    return redirect(request.META.get("HTTP_REFERER"))
