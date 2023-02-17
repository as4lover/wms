from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from customer.models import User
from company.models import AddressBook
from .forms import AddressBookFormSet, EditAddressForm

# ==== Customer Address ====
@login_required(login_url="account_login")
def create_customer_address(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customer = User.objects.get(id=pk_id)
    address = AddressBook.objects.filter(user__username=customer.username)
    formset = AddressBookFormSet(request.POST or None)
    if request.method == "POST":
        if formset.is_valid():
            formset.instance = customer
            formset.save()
            return redirect("storeman:display_customer_details", pk_id=customer.id)

    context = {"formset": formset, "customer": customer, "address": address}

    return render(request, "storeman/customer/create_customer_address.html", context)


@login_required(login_url="account_login")
def edit_customer_address(request, pk_id, addr_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customer = User.objects.get(id=pk_id)
    address = AddressBook.objects.get(user__username=customer.username, id=addr_id)
    if request.method == "POST":
        form = EditAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("storeman:display_customer_details", pk_id=pk_id)
    else:
        form = EditAddressForm(instance=address)
    context = {"form": form, "customer": customer, "address": address}
    return render(request, "storeman/customer/edit_customer_address.html", context)


@login_required(login_url="account_login")
def delete_customer_address(request, pk_id, addr_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    customer = User.objects.get(id=pk_id)
    address = AddressBook.objects.get(user__username=customer.username, id=addr_id)
    address.delete()
    return redirect("storeman:display_customer_details", pk_id=pk_id)
