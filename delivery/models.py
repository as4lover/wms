from django.db import models
from customer.models import User


class StaffMember(models.Model):
    SYD_REGION = [
        ("동부팀", "동부팀"),
        ("서부팀", "서부팀"),
        ("남부팀", "남부팀"),
        ("북부팀", "북부팀"),
        ("외곽팀", "외곽팀"),
        ("고맙스", "고맙스"),
    ]
    POSITION_LIST = [
        ("팀장", "팀장"),
        ("차장", "차장"),
        ("과장", "과장"),
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
