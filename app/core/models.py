from django.db import models
from django.utils import timezone

class Business(models.Model):
    business_name = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    lic_expir_dd = models.DateField()
    license_creation_date = models.DateField()
    license_status = models.CharField(max_length=255, null=True)
    license_type = models.CharField(max_length=255, null=True)
    address_city = models.CharField(max_length=255, null=True)
    address_state = models.CharField(max_length=255, null=True)
    address_borough = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.business_name:
            return self.business_name
        return self.industry