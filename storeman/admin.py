from django.contrib import admin
from storeman.models import UserOrder, UserOrderItem


# @admin.register(CreateUserOrder)
# class CreateUserOrderAdmin(admin.ModelAdmin):
#     list_display = ("customer", "status", "driver")


# @admin.register(UserOrderItem)
# class UserOrderItemAdmin(admin.ModelAdmin):
#     list_display = ("order", "product", "quantity", "order_code")


class UserOrderItemInlineAdmin(admin.TabularInline):
    model = UserOrderItem


class UserOrderAdmin(admin.ModelAdmin):
    inlines = [UserOrderItemInlineAdmin]
    list_display = [
        "customer",
        "address",
    ]


admin.site.register(UserOrder, UserOrderAdmin)
