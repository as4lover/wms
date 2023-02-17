from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ("ADMIN", "admin"),
    ("MANAGER", "Manager"),
    ("DRIVER", "Driver"),
    ("CUSTOMER", "Customer"),
)


class User(AbstractUser):
    phone = models.CharField(max_length=10, unique=True, null=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=None, blank=True, null=True
    )

    def __str__(self):
        return f"{self.username}"
