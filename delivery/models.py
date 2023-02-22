from django.db import models
from customer.models import User


class StaffMember(models.Model):
    SYD_REGION = [
        ("EAST", "동부"),
        ("WEST", "서부"),
        ("SOUTH", "남부"),
        ("NORTH", "북부"),
        ("REGINE", "외곽"),
        ("GOMAPS", "고맙스"),
    ]
    POSITION_LIST = [
        ("부장", "부장"),
        ("차장", "차장"),
        ("대리", "대리"),
    ]
    name = models.ForeignKey(User, on_delete=models.PROTECT)
    region = models.CharField(max_length=10, choices=SYD_REGION, null=True, blank=True)
    is_status = models.BooleanField(default=True, blank=True)
    position = models.CharField(
        max_length=30, choices=POSITION_LIST, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.name.last_name}{self.name.first_name}"
