from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .filters import ProductFilter
from store.models import Product
from .forms import ProductForm


@login_required(login_url="account_login")
def product_list(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    products = Product.objects.all().order_by("-created_at")
    product_filter = ProductFilter(request.GET, queryset=products)
    products_qs = product_filter.qs
    page_num = request.GET.get("page", 1)
    paginator = Paginator(products_qs, 10)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    lefIndex = int(page_num) - 5
    if lefIndex < 1:
        lefIndex = 1

    rightIndex = int(page_num) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(lefIndex, rightIndex)

    context = {
        "page_num": page_num,
        "products_qs": products_qs,
        "page_obj": page_obj,
        "paginator": paginator,
        "custom_range": custom_range,
        "product_filter": product_filter,
    }
    return render(request, "storeman/product/product_list.html", context)


@login_required(login_url="account_login")
def create_product(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("storeman:product_list")
    context = {"form": form}
    return render(request, "storeman/product/create_product.html", context)


@login_required(login_url="account_login")
def display_product_detail(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    product = Product.objects.get(id=pk_id)
    context = {"product": product}
    return render(request, "storeman/product/display_product_detail.html", context)


@login_required(login_url="account_login")
def edit_product(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    product = Product.objects.get(id=pk_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("storeman:edit_product", pk_id=pk_id)
    else:
        form = ProductForm(instance=product)
    context = {"form": form, "product": product}
    return render(request, "storeman/product/edit_product.html", context)


@login_required(login_url="account_login")
def delete_product(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    product = Product.objects.get(id=pk_id)
    product.delete()
    return redirect("storeman:product_list")
