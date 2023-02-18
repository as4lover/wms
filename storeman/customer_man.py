from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from customer.models import User
from company.models import AddressBook
from .forms import CreateUserForm, EditUserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# === Customer Info ==================
@login_required(login_url="account_login")
def create_customer(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("storeman:display_customer_list")
    context = {"form": form}
    return render(request, "storeman/customer/create_customer.html", context)
    # return render(request, "storeman/includes/modal_create_customer.html", context)


@login_required(login_url="account_login")
def edit_customer(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customer = User.objects.get(id=pk_id)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("storeman:display_customer_details", pk_id=pk_id)
    else:
        form = EditUserForm(instance=customer)
    context = {"form": form, "customer": customer}
    return render(request, "storeman/customer/edit_customer.html", context)


@login_required(login_url="account_login")
def delete_customer(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customer = User.objects.get(id=pk_id)
    customer.delete()
    return redirect("storeman:display_customer_list")


@login_required(login_url="account_login")
def display_customer_list(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customers = AddressBook.objects.filter(
        user__is_staff=False, user__is_superuser=False, default=True
    ).order_by("user__last_login")
    page = request.GET.get("page", 1)
    paginator = Paginator(customers, 10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    lefIndex = int(page) - 5
    if lefIndex < 1:
        lefIndex = 1

    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(lefIndex, rightIndex)

    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "custom_range": custom_range,
    }

    return render(request, "storeman/customer/display_customer_list.html", context)


@login_required(login_url="account_login")
def display_customer_details(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customer = User.objects.get(id=pk_id)
    address = AddressBook.objects.filter(user__username=customer.username)
    context = {
        "customer": customer,
        "address": address,
    }
    return render(request, "storeman/customer/display_customer_details.html", context)
