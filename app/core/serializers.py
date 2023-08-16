from rest_framework import serializers
from core.models import Business


class CustomDateTimeField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value.isoformat()


class BusinessSerializer(serializers.ModelSerializer):
    lic_expir_dd = CustomDateTimeField()
    license_creation_date = CustomDateTimeField()

    class Meta:
        model = Business
        fields = [
            "id",
            "business_name",
            "industry",
            "lic_expir_dd",
            "license_creation_date",
            "license_status",
            "license_type",
            "address_city",
            "address_state",
            "address_borough",
        ]
