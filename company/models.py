from django.db import models
from delivery.models import StaffMember


class BusinessType(models.Model):
    biz_type = models.CharField(max_length=30, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.biz_type}"


class AddressBook(models.Model):
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
    user = models.ForeignKey(
        "customer.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    nick_name = models.CharField(max_length=10, null=True, blank=True)
    h_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    e_name = models.CharField(max_length=100, null=True, blank=True)
    biz_type = models.ForeignKey(
        BusinessType, on_delete=models.SET_NULL, null=True, blank=True
    )
    address = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=3, choices=aus_state, default="NSW")
    city = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=False)
    delivery_instructions = models.CharField(max_length=255, null=True, blank=True)
    driver = models.ForeignKey(
        StaffMember, null=True, blank=True, on_delete=models.CASCADE
    )
    vegi_code = models.CharField(max_length=6, null=True, unique=True, blank=True)
    gen_code = models.CharField(max_length=6, null=True, unique=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.address}"
