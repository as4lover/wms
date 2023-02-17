from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "company"

urlpatterns = [
    # My information
    path("my_dashboard/", views.my_dashboard, name="my_dashboard"),
    path("my_address/", views.my_addressbook, name="my_addressbook"),
    # path("add_address", views.add_address, name="add_address"),
    path("my_address/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("my_address/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("my_address/set_default/<slug:id>/", views.set_default, name="set_default"),
]
