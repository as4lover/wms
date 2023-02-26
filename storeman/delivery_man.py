from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from delivery.models import StaffMember
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2 import RequestConfig
from storeman.tables import StaffMemberTable
from customer.models import User
from .forms import EditDeliveryTeamForm


@login_required(login_url="account_login")
def display_delivery_team(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    team = StaffMember.objects.filter(name__is_active=True)
    context = {"team": team}
    return render(request, "storeman/delivery/display_delivery_team.html", context)


@login_required(login_url="account_login")
def edit_delivery_team(request, pk_id):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    team = StaffMember.objects.get(id=pk_id)
    if request.method == "POST":
        form = EditDeliveryTeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect("storeman:display_delivery_team")
    else:
        form = EditDeliveryTeamForm(instance=team)
    context = {"form": form, "team": team}
    return render(request, "storeman/delivery/edit_delivery_team.html", context)
