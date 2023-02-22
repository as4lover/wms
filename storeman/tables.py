import django_tables2 as tables
from customer.models import User


class StaffMemberTable(tables.Table):
    class Meta:
        model = User
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
