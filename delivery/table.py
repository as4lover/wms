import django_tables2 as tables
from store.models import Order, OrderItem
from django.utils.html import format_html


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<img src="/media/{url}" height="50" class="delivery_photo">',
            url=value,
        )


class MyDeliveryTable(tables.Table):
    tracking_no = tables.Column(verbose_name="#")
    company_name = tables.Column(verbose_name="고객")
    delivery_photo = ImageColumn(verbose_name="사진")
    updated_at = tables.DateTimeColumn(verbose_name="시간")

    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap4-responsive.html"
        sequence = (
            "tracking_no",
            "company_name",
            "payment_mode",
        )
        exclude = (
            "id",
            "user",
            "company_e_name",
            "city",
            "fname",
            "lname",
            "phone",
            "email",
            "address",
            "state",
            "postcode",
            "total_price",
            "payment_mode",
            "payment_id",
            "message",
            "barcode_img",
            "ami_file",
            "ami_daily_file",
            "order_pdf",
            "pdf_daily_file",
            "driver",
            "driver_first_name",
            "driver_last_name",
            "created_at",
            "status",
            "delivery_note",
        )

    # 추가컬럼
    view = tables.TemplateColumn(
        template_name="delivery/my_delivery_detail_column.html",
        verbose_name="보기",
        orderable=False,
    )


class MyDeliveryDetailTable(tables.Table):
    product = tables.Column(verbose_name="제품")
    quantity = tables.Column(verbose_name="수량")
    item_status = tables.Column(verbose_name="상태")

    class Meta:
        model = OrderItem
        template_name = "django_tables2/bootstrap4-responsive.html"
        exclude = ("id", "order", "price", "order_code", "order_type")
