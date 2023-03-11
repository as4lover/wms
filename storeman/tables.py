import django_tables2 as tables
from customer.models import User
from store.models import Order, DailyJobs


class StaffMemberTable(tables.Table):
    username = tables.Column(verbose_name="사용자ID")
    last_name = tables.Column(verbose_name="성")
    first_name = tables.Column(verbose_name="이름")
    email = tables.Column(verbose_name="이메일")
    phone = tables.Column(verbose_name="전화번호")
    role = tables.Column(verbose_name="역할")
    is_active = tables.Column(verbose_name="근무중")
    last_login = tables.Column(verbose_name="최근로그인")

    class Meta:
        model = User
        attrs = {
            "class": "table table-hover",
            "thead": {"class": "table-warning"},
        }
        template_name = "django_tables2/bootstrap5.html"
        sequence = (
            "username",
            "last_name",
            "first_name",
            "email",
            "phone",
            "role",
            "is_active",
        )
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "date_joined",
        )

    # 추가 컬럼
    edit = tables.TemplateColumn(
        template_name="storeman/staff/staff_edit_column.html",
        verbose_name="수정",
        orderable=False,  # Sorting 안되게
    )


### Order Table
class OrderListTable(tables.Table):
    tracking_no = tables.Column(verbose_name="주문번호")
    company_name = tables.Column(verbose_name="회사명")
    company_e_name = tables.Column(verbose_name="회사명(E)")
    address = tables.Column(verbose_name="주소")
    city = tables.Column(verbose_name="도시")
    state = tables.Column(verbose_name="주")
    status = tables.Column(verbose_name="배송상태")
    message = tables.Column(verbose_name="고객전달")
    created_at = tables.Column(verbose_name="주문시간")
    updated_at = tables.Column(verbose_name="수정시간")

    class Meta:
        model = Order
        attrs = {
            "class": "table table-hover",
            "thead": {"class": "table-secondary"},
        }
        template_name = "django_tables2/bootstrap5.html"
        sequence = (
            "tracking_no",
            "company_name",
            "company_e_name",
        )
        exclude = (
            "id",
            "user",
            "phone",
            "total_price",
            "payment_mode",
            "payment_id",
            "barcode_img",
            "ami_daily_file",
            "ami_file",
            "order_pdf",
            "driver",
            "driver_first_name",
            "driver_last_name",
            "delivery_note",
            "delivery_photo",
            "fname",
            "lname",
            "email",
            "state",
            "postcode",
            "address",
            "city",
            "pdf_daily_file",
        )

    view = tables.TemplateColumn(
        template_name="storeman/order/order_list_view_column.html",
        verbose_name="보기",
        orderable=False,
    )


## DAily Jobs table
class dailyOrderTable(tables.Table):
    class Meta:
        model = DailyJobs
        attrs = {
            "class": "table table-hover",
        }
        sequence = (
            "daily_merged_csv",
            "daily_merged_pdf",
            "created_user",
            "created_at",
        )
        exclude = ("id",)
        template_name = "django_tables2/bootstrap5.html"
