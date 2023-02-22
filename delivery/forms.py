from django.forms import ModelForm, TextInput
from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import StaffMember
from customer.models import User
from store.models import Order, OrderItem


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            "status",
            "delivery_note",
        ]
        widgets = {
            "delivery_note": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "status": "배송상태",
            "delivery_note": "특이사항",
        }


class ItemStatusForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            "item_status",
        ]


