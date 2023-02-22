from django.contrib import admin
from .models import *


@admin.register(StaffMember)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "region",
    ]
