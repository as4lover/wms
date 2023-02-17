from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from delivery.models import StaffMember
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# === Staff Info ==================
@login_required(login_url="account_login")
def display_staff(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    members = StaffMember.objects.all()
    context = {"members": members}
    return render(request, "storeman/staff/display_staff.html", context)
