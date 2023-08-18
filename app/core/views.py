"""
Endpoints logic
"""
from typing import Optional
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from core.serializers import BusinessSerializer
from core.models import Business
from rest_framework import serializers
from datetime import datetime


def data_filter_validation(request) -> Optional[Response]:
    if (
        not request.GET.get("begin_date")
        and not request.GET.get("end_date")
        and not request.GET.get("license_date_type")
    ):
        instance = Business.objects.all()
        serializer = BusinessSerializer(instance, many=True)
        count_businesses = instance.count()
        return Response(
            {"number_of_businesses": count_businesses, "businesses": serializer.data}
        )
    return None


# helper function for businesses filtering
def business_by(request, filter_type):
    filter_kwargs = {}
    filter_name = ""

    if (
        not request.GET.get("license_date_type")
        and not request.GET.get("begin_date")
        and not request.GET.get("end_date")
    ):
        filter_type_val = request.GET.get(f"{filter_type}")
        filter_kwargs[f"{filter_type}"] = filter_type_val
        instance = Business.objects.filter(**filter_kwargs)
        count_businesses = Business.objects.filter(**filter_kwargs).count()
        serializer = BusinessSerializer(instance, many=True)
        return Response(
            {"number_of_businesses": count_businesses, "businesses": serializer.data}
        )
    elif (
        request.GET.get("license_date_type")
        and not request.GET.get("begin_date")
        or not request.GET.get("end_date")
    ):
        return Response(
            {"error": "Please provide begin_date and end_date."}, status=400
        )
    elif (
        not request.GET.get("license_date_type")
        and request.GET.get("begin_date")
        and request.GET.get("end_date")
    ):
        return Response({"error": "Please provide license_date_type."}, status=400)

    filter_type_val = request.GET.get(f"{filter_type}")
    license_date_type = request.GET.get("license_date_type")
    start_date_str = request.GET.get("begin_date")
    end_date_str = request.GET.get("end_date")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    if license_date_type == "Creation":
        filter_name = "license_creation_date"
    else:
        filter_name = "lic_expir_dd"

    filter_kwargs[f"{filter_type}"] = filter_type_val
    filter_kwargs[f"{filter_name}__gte"] = start_date
    filter_kwargs[f"{filter_name}__lte"] = end_date

    instance = Business.objects.filter(**filter_kwargs)
    count_businesses = Business.objects.filter(**filter_kwargs).count()
    serializer = BusinessSerializer(instance, many=True)
    return Response(
        {"number_of_businesses": count_businesses, "businesses": serializer.data}
    )


@extend_schema(
    description="Get all businesess or by the range of their license creation/expiration dates. Date format should be like: yyyy-mm-dd",
    parameters=[
        OpenApiParameter("begin_date", OpenApiTypes.STR, required=False),
        OpenApiParameter("end_date", OpenApiTypes.STR, required=False),
        OpenApiParameter(
            "license_date_type",
            OpenApiTypes.STR,
            required=False,
            enum=["Creation", "Expiration"],
        ),
    ],
    responses=BusinessSerializer,
)
@api_view(["GET"])
def business_list(request):
    if invalid_date_input := data_filter_validation(request):
        return invalid_date_input

    elif (
        request.GET.get("license_date_type")
        and not request.GET.get("begin_date")
        or not request.GET.get("end_date")
    ):
        return Response(
            {"error": "Please provide begin_date and end_date."}, status=400
        )
    elif (
        not request.GET.get("license_date_type")
        and request.GET.get("begin_date")
        and request.GET.get("end_date")
    ):
        return Response({"error": "Please provide license_date_type."}, status=400)

    filter_kwargs = {}
    license_date_type = request.GET.get("license_date_type")
    start_date_str = request.GET.get("begin_date")
    end_date_str = request.GET.get("end_date")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    if license_date_type == "Creation":
        filter_name = "license_creation_date"
    else:
        filter_name = "lic_expir_dd"

    filter_kwargs[f"{filter_name}__gte"] = start_date
    filter_kwargs[f"{filter_name}__lte"] = end_date

    instance = Business.objects.filter(**filter_kwargs)
    count_businesses = Business.objects.filter(**filter_kwargs).count()
    serializer = BusinessSerializer(instance, many=True)
    return Response(
        {"number_of_businesses": count_businesses, "businesses": serializer.data}
    )


@extend_schema(
    description="Get businesses by license status and range of license creation/expiration dates. Date format should be like: yyyy-mm-dd",
    parameters=[
        OpenApiParameter("begin_date", OpenApiTypes.STR, required=False),
        OpenApiParameter("end_date", OpenApiTypes.STR, required=False),
        OpenApiParameter(
            "license_date_type",
            OpenApiTypes.STR,
            required=False,
            enum=["Creation", "Expiration"],
        ),
        OpenApiParameter(
            "license_status",
            OpenApiTypes.STR,
            required=True,
            enum=["Active", "Inactive"],
        ),
    ],
    responses=BusinessSerializer,
)
@api_view(["GET"])
def business_license_status(request):
    return business_by(request, filter_type="license_status")


@extend_schema(
    description="Get businesses by license status and range of license creation/expiration dates. Date format should be like: yyyy-mm-dd",
    parameters=[
        OpenApiParameter("begin_date", OpenApiTypes.STR, required=False),
        OpenApiParameter("end_date", OpenApiTypes.STR, required=False),
        OpenApiParameter(
            "license_date_type",
            OpenApiTypes.STR,
            required=False,
            enum=["Creation", "Expiration"],
        ),
        OpenApiParameter(
            "license_type",
            OpenApiTypes.STR,
            required=True,
            enum=["Business", "Individual"],
        ),
    ],
    responses=BusinessSerializer,
)
@api_view(["GET"])
def business_license_type(request):
    return business_by(request, filter_type="license_type")
