from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django import template

from xhtml2pdf import pisa

from django.template.loader import render_to_string
from weasyprint import HTML


def xhtml_render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding="UTF-8")
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def weasypdf_render_to_pdf(template_src, context_dict):
    html = render_to_string(template_src, context_dict)
    out = BytesIO()
    html = HTML(string=html).write_pdf(out)
    return None

