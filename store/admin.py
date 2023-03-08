from django.contrib import admin
from .models import *


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "order_code"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "e_title"]
    prepopulated_fields = {"slug": ("title",)}  # title 필드입력동시에 slug필드자동입력


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["category"]
    list_display = [
        "title",
        "e_title",
        "category",
        "bar_code",
        "per_box",
        "unit",
        "spec",
        "is_active",
        "created_at",
        "updated_at",
    ]
    search_fields = ["title", "e_title"]
    list_editable = ["category", "is_active"]
    # prepopulated_fields = {"slug": ("title",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "company_name",
        "tracking_no",
        "status",
        "driver",
        "driver_last_name",
        "driver_first_name",
        "message",
        "ami_file",
        "order_pdf",
        "ami_daily_file",
        "delivery_photo",
    )
    list_editable = [
        "status",
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "order_code",
        "order_type",
        "product",
        "price",
        "quantity",
    )


@admin.register(OrderCode)
class OrderCodeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "address",
        "order_type",
    ]


@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]


@admin.register(DailyJobs)
class DailyJobsAdmin(admin.ModelAdmin):
    list_display = [
        "created_user",
        "daily_merged_csv",
        "daily_merged_pdf",
        "created_at",
    ]
