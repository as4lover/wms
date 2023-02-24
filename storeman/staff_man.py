from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from delivery.models import StaffMember
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2 import RequestConfig
from storeman.tables import StaffMemberTable
from customer.models import User
from .forms import CreateStaffForm, CreateDriverFormSet, EditStaffForm

# === Staff Info ==================
@login_required(login_url="account_login")
def display_staff(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    members = User.objects.filter(is_staff=True).exclude(is_superuser=True)
    table = StaffMemberTable(members)
    RequestConfig(request, paginate={"per_page": 5}).configure(
        table
    )  # tables2 sorting 위해
    context = {
        "table": table,
    }
    template_name = "storeman/staff/display_staff.html"

    return render(request, template_name, context)


def create_staff(request):
    form = CreateStaffForm()
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("storeman:display_staff")
    context = {"form": form}
    return render(request, "storeman/staff/create_staff.html", context)


def edit_staff(request, pk_id):
    staff = User.objects.get(id=pk_id)
    if request.method == "POST":
        form = EditStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect("storeman:display_staff")
    else:
        form = EditStaffForm(instance=staff)
    context = {"form": form, "staff": staff}
    return render(request, "storeman/staff/edit_staff.html", context)


def create_driver(request, pk_id):
    staff = User.objects.get(id=pk_id)
    driver = StaffMember.objects.filter(name__username=staff.username)
    formset = CreateDriverFormSet(request.POST or None)
    if request.method == "POST":
        if formset.is_valid():
            formset.instance = staff
            formset.save()
            return redirect("storeman:display_staff")
    context = {"formset": formset, "staff": staff, "driver": driver}
    return render(request, "storeman/staff/create_driver.html", context)
