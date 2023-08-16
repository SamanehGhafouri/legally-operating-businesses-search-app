from core import views
from django.urls import path


urlpatterns = [
    path("", views.business_list, name="business_list"),
    path("status/", views.business_license_status, name="status"),
]
