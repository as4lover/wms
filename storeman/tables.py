import django_tables2 as tables
from delivery.models import StaffMember


class StaffMemberTable(tables.Table):
    class Meta:
        model = StaffMember
        template_name = "django_tables2/bootstrap.html"
