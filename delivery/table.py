import django_tables2 as tables
from store.models import Order
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
    payment_mode = tables.Column(verbose_name="수금")
    delivery_photo = ImageColumn(verbose_name="사진")

    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap-responsive.html"
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
            "updated_at",
            "delivery_note",
        )
