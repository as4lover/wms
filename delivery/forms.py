from django.forms import ModelForm, TextInput, inlineformset_factory
from django import forms
from .models import StaffMember
from customer.models import User
from store.models import Order, OrderItem


class OrderForm(ModelForm):
    STATUS = (
        ("", "선택"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )
    PAYMENT = (
        ("", "선택"),
        ("수금", "수금"),
        ("미수금", "미수금"),
    )
    status = forms.ChoiceField(label="배송상태", choices=STATUS)
    payment_mode = forms.ChoiceField(label="결제상태", choices=PAYMENT)
    delivery_photo = forms.ImageField(required=False)
    class Meta:
        model = Order
        fields = [
            "status",
            "delivery_note",
            "payment_mode",
            "delivery_photo",
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
    STATUS = (
        ("정상", "정상"),
        ("반품", "반품"),
        ("미배달", "미배달"),
    )
    item_status = forms.ChoiceField(label="상태", choices=STATUS)

    class Meta:
        model = OrderItem
        fields = [
            "item_status",
        ]
