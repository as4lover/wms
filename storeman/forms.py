from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from customer.models import User
from company.models import AddressBook
from store.models import OrderCode, Product
from django import forms
from .models import *


class AddUserAddressForm(ModelForm):
    class Meta:
        model = AddressBook
        fields = "__all__"


AddressBookFormSet = inlineformset_factory(
    User,
    AddressBook,
    form=AddUserAddressForm,
    min_num=1,
    extra=1,
    can_delete=False,
)


class EditAddressForm(ModelForm):
    class Meta:
        model = AddressBook
        fields = "__all__"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        ]


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]


class OrderForm(ModelForm):
    class Meta:
        model = UserOrder
        fields = "__all__"


class OrderItemForm(ModelForm):
    class Meta:
        model = UserOrderItem
        fields = "__all__"


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class OrderCodeForm(ModelForm):
    class Meta:
        model = OrderCode
        fields = "__all__"
