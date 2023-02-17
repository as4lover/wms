from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls import url, handler400, handler403, handler404, handler500


urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # Store management
    path("storeman/", include("storeman.urls")),
    # Delivery management
    # Store management
    path("delivery/", include("delivery.urls")),
    # customer
    path("account/", include("customer.urls")),
    # company
    path("company/", include("company.urls")),
    path("", include("store.urls")),
    # allauth
    path(
        "email-confirmation-done/",
        TemplateView.as_view(template_name="account/email-confirmation-done.html"),
        name="account_email_confirmation_done",
    ),
    path("", include("allauth.urls")),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "django.views.defaults.bad_request"
handler403 = "django.views.defaults.permission_denied"
handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
