from django.shortcuts import redirect, render, HttpResponseRedirect
from .models import AddressBook
from store.cart import *


@login_required(login_url="account_login")
def my_dashboard(request):
    return render(request, "myinfo/myinfo_home.html")


# My addressbooks
@login_required(login_url="account_login")
def my_addressbook(request):
    address = AddressBook.objects.filter(user=request.user).order_by("-id")
    return render(request, "myinfo/myinfo_addressbook.html", {"address": address})


# Edit


@login_required(login_url="account_login")
def edit_address(request, id):
    if request.method == "POST":
        address = AddressBook.objects.get(pk=id, user=request.user)
        address_form = AddressBookForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("company:my_addressbook"))
    else:
        address = AddressBook.objects.get(pk=id, user=request.user)
        address_form = AddressBookForm(instance=address)
    return render(request, "myinfo/add_address.html", {"form": address_form})


# delete_address
@login_required(login_url="account_login")
def delete_address(request, id):
    address = AddressBook.objects.filter(pk=id, user=request.user).delete()
    return redirect("company:my_addressbook")


# Set default


@login_required(login_url="account_login")
def set_default(request, id):
    # OrderCode.objects.filter(user=request.user, default=True).update(default=False)
    AddressBook.objects.filter(user=request.user, default=True).update(default=False)
    AddressBook.objects.filter(pk=id, user=request.user).update(default=True)
    # OrderCode.objects.filter(user=request.user, pk=id).update(default=True)
    # return redirect("company:my_addressbook")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
