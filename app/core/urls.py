from core import views
from django.urls import path


urlpatterns = [
    path("", views.business_list, name="business_list"),
    path("license-status/", views.business_license_status, name="status"),
    path("license-type/", views.business_license_type, name="type"),
]
