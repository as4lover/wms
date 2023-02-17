import django_filters
from store.models import Product
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

    #     labels = {
    #         "title": "제품명(한글)",
    #         "e_title": "제품명(영문)",
    #         "category": "카테고리",
    #     }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column("title__icontains", css_class="form col-md-3 mb-0"),
    #             Column("e_title__icontains", css_class="form col-md-3 mb-0"),
    #             Column("category", css_class="form col-md-3 mb-0"),
    #         ),
    #     )
