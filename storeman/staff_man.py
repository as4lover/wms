from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from delivery.models import StaffMember
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from storeman.tables import StaffMemberTable

# === Staff Info ==================
@login_required(login_url="account_login")
def display_staff(request):
    if not request.user.is_staff | request.user.is_superuser:
        return redirect("/login")
    members = StaffMember.objects.all()
    table = StaffMemberTable(members)
    context = {
        "table": table,
    }
    template_name = "storeman/staff/display_staff.html"

    return render(request, template_name, context)
