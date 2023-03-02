import django_filters
from store.models import Product, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "title": ["icontains"],
            "e_title": ["icontains"],
            "is_active": ["exact"],
            "category": ["exact"],
        }


class OrderListFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            "created_at": ["exact"],
            "status": ["exact"],
        }
