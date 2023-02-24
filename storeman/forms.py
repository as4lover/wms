from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from customer.models import User
from company.models import AddressBook
from store.models import OrderCode, Product
from delivery.models import StaffMember
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
            "is_active",
        ]


# Staff
class CreateStaffForm(UserCreationForm):
    ROLE = (
        ("", "선택..."),
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("DRIVER", "Driver"),
    )
    username = forms.CharField(label="UserID", widget=forms.TextInput())
    password1 = forms.CharField(label="패스워드", widget=forms.PasswordInput())
    password2 = forms.CharField(label="패스워드확인", widget=forms.PasswordInput())
    first_name = forms.CharField(label="이름", widget=forms.TextInput())
    last_name = forms.CharField(label="성명", widget=forms.TextInput())
    email = forms.EmailField(label="이메일", widget=forms.TextInput())
    phone = forms.CharField(label="전화번호", max_length=10, widget=forms.TextInput())
    role = forms.ChoiceField(label="역할", choices=ROLE)
    is_active = forms.BooleanField(label="근무중", required=True)
    is_staff = forms.BooleanField(label="직원", required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "is_active",
            "is_staff",
        ]


class AddDeliveryStaffForm(ModelForm):
    class Meta:
        model = StaffMember
        fields = "__all__"


CreateDriverFormSet = inlineformset_factory(
    User,
    StaffMember,
    form=AddDeliveryStaffForm,
    min_num=1,
    extra=1,
    can_delete=False,
)


class EditStaffForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "is_active",
            "is_staff",
        ]


# Order
class OrderForm(ModelForm):
    class Meta:
        model = UserOrder
        fields = "__all__"


class OrderItemForm(ModelForm):
    class Meta:
        model = UserOrderItem
        fields = "__all__"


class OrderCodeForm(ModelForm):
    class Meta:
        model = OrderCode
        fields = "__all__"


# Product
class ProductForm(ModelForm):
    list_price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    sale_price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    quantity = forms.IntegerField()
    per_box = forms.IntegerField()

    class Meta:
        model = Product
        fields = [
            "title",
            "e_title",
            "category",
            "bar_code",
            "location",
            "list_price",
            "sale_price",
            "quantity",
            "description",
            "brand",
            "unit",
            "spec",
            "color",
            "per_box",
            "tag",
            "image",
            "is_active",
        ]
        labels = {
            "title": "제품명(한글)",
            "e_title": "제품명(영문)",
            "category": "제품목록",
            "bar_code": "바코드",
            "location": "창고위치",
            "color": "색깔",
            "per_box": "박스당갯수",
            "tag": "태그",
            "is_active": "판매중",
        }
