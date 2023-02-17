from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import BusinessType, AddressBook


@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):
    list_display = [
        "nick_name",
        "h_name",
        "e_name",
        "biz_type",
        "address",
        "representative",
        "vegi_code",
        "gen_code",
    ]


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ["biz_type"]
