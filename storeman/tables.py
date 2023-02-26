from django_tables2 import tables, TemplateColumn
from customer.models import User


class StaffMemberTable(tables.Table):
    class Meta:
        model = User
        attrs = {"class": "table table-sm"}
        template_name = "django_tables2/bootstrap-responsive.html"
        sequence = (
            "id",
            "username",
            "last_name",
            "first_name",
            "email",
            "phone",
            "role",
            "is_active",
        )
        exclude = ("password", "is_superuser", "is_staff", "date_joined")

    edit = TemplateColumn(
        template_name="storeman/staff/staff_edit_column.html", orderable=False
    )
