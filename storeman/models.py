from django.db import models

# from storeman.models import CreateUserOrder
from store.models import Product
from customer.models import User
from company.models import AddressBook
from delivery.models import StaffMember


class UserOrder(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    address = models.ForeignKey(AddressBook, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=200, null=True, default="Pending", choices=STATUS
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"self.customer"


class UserOrderItem(models.Model):
    order = models.ForeignKey(UserOrder, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return f"self.order"
