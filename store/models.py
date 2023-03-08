from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
from customer.models import User
from company.models import AddressBook
from django.core.files import File


import barcode
from barcode.writer import ImageWriter
from io import BytesIO


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=100, unique=True, null=True)
    e_title = models.CharField(_("e_title"), max_length=100, null=True)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True, allow_unicode=True)
    image = models.ImageField(
        _("Image"),
        upload_to="images/category",
        default="images/category/default.png",
        blank=True,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        ordering = ("title",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    e_title = models.CharField(
        _("English Title"), max_length=100, null=True, blank=True
    )
    # slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    bar_code = models.CharField(_("BAR Code"), max_length=6, blank=True, null=True)
    location = models.CharField(_("Location"), max_length=6, blank=True, null=True)
    list_price = models.DecimalField(
        _("List Price"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    sale_price = models.DecimalField(
        _("Sale Price"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    quantity = models.IntegerField(_("Quantity"), null=True, blank=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    brand = models.CharField(_("Brand"), max_length=100, null=True, blank=True)
    unit = models.CharField(_("Unit"), max_length=20, null=True, blank=True)
    spec = models.CharField(_("Spec"), max_length=20, null=True, blank=True)
    color = models.CharField(_("Color"), max_length=10, null=True, blank=True)
    per_box = models.IntegerField(_("Per Box"), null=True, blank=True)
    tag = models.CharField(_("Tag"), max_length=150, null=True, blank=True)

    image = models.ImageField(
        _("Image"),
        upload_to="images/product",
        default="images/product/default.png",
        blank=True,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["location"]
        verbose_name_plural = "Products"
        index_together = [["id", "title"]]

    def __str__(self):
        return f"{self.title}"


class OrderCode(models.Model):

    order_key = (
        ("일반", "일반"),
        ("야채", "야채"),
        ("주류", "주류"),
    )
    code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    order_type = models.CharField(max_length=10, choices=order_key, default="일반")
    address = models.ForeignKey(
        AddressBook, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.code},{self.address},{self.order_type}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order_code = models.CharField(max_length=6, null=True, blank=True)


class Order(models.Model):
    aus_state = (
        ("NSW", "NSW"),
        ("VIC", "VIC"),
        ("QLD", "QLD"),
        ("ACT", "ACT"),
        ("SA", "SA"),
        ("WA", "WA"),
        ("NT", "NT"),
        ("TAS", "TAS"),
    )

    order_status = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )
    PAYMENT = (
        ("수금", "수금"),
        ("미수금", "미수금"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, null=False)
    company_e_name = models.CharField(max_length=150, blank=True, null=True)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=3, choices=aus_state, default="NSW")
    postcode = models.CharField(max_length=4, null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=150, choices=PAYMENT, null=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=150, choices=order_status, default="Pending")
    message = models.TextField(null=True, blank=True)
    tracking_no = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barcode_img = models.ImageField(upload_to="order/barcode/%Y/%m/%d/", blank=True)
    ami_file = models.FileField(upload_to="order/ami/%Y/%m/%d/", blank=True)
    ami_daily_file = models.FileField(upload_to="order/daily/", blank=True)
    order_pdf = models.FileField(upload_to="order/pdf/%Y/%m/%d/", blank=True)
    pdf_daily_file = models.FileField(upload_to="order/daily", blank=True)
    driver = models.CharField(max_length=100, blank=True)
    driver_first_name = models.CharField(max_length=50, blank=True)
    driver_last_name = models.CharField(max_length=50, blank=True)
    delivery_note = models.TextField(null=True, blank=True)
    delivery_photo = models.ImageField(
        verbose_name="사진업로드", upload_to="order/delivery/%Y/%m/%d", blank=True
    )

    def __str__(self):
        return f"{self.id}, {self.tracking_no},{self.barcode_img}"

    def delete(self, *args, **kwargs):
        self.barcode_img.delete()
        self.ami_file.delete()
        self.order_pdf.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):
    STATUS = (
        ("정상", "정상"),
        ("반품", "반품"),
        ("미배달", "미배달"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(null=False)
    order_code = models.CharField(max_length=6, null=True, blank=True)
    order_type = models.CharField(max_length=10, null=True, blank=True)
    item_status = models.CharField(
        max_length=100, null=True, blank=True, choices=STATUS, default="정상"
    )
    # 제품위치별 정렬
    class Meta:
        ordering = ["product"]

    def __str__(self):
        return f"{self.order.id}"

    # 주문한 갯수 x 제품가격
    def get_item_price(self):
        return self.price * self.quantity


# Wishlist (자주주문제품)


class WishItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"


# Daily Order 처리


class DailyJobs(models.Model):
    created_user = models.ForeignKey(
        User, verbose_name=_("작성자"), on_delete=models.CASCADE, null=True
    )
    daily_merged_csv = models.FileField(
        verbose_name=_("알맹이CSV"), upload_to="order/daily/csv/%Y/%m/%d/", blank=True
    )
    daily_merged_pdf = models.FileField(
        verbose_name=_("주문서PDF"), upload_to="order/daily/pdf/%Y/%m/%d", blank=True
    )
    created_at = models.DateTimeField(verbose_name=_("작성일"), auto_now_add=True)

    def __str__(self):
        return f"{self.created_user}"
