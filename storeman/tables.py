from django_tables2 import tables, TemplateColumn
from customer.models import User


class StaffMemberTable(tables.Table):
    class Meta:
        model = User
        attrs = {"class": "table table-sm"}
        template_name = "django_tables2/bootstrap.html"
        sequence = (
            "username",
            "last_name",
            "first_name",
            "email",
            "phone",
            "role",
        )
        exclude = ("password",)

    edit = TemplateColumn(
        template_name="storeman/staff/staff_edit_column.html", orderable=False
    )
