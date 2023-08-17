"""
Endpoints logic
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from core.serializers import BusinessSerializer
from core.models import Business
from rest_framework import serializers
from datetime import datetime


@extend_schema(
    description="Get all businesess or by the range of their license creation/expiration dates. Date format should be like: yyyy-mm-dd",
    parameters=[
        OpenApiParameter(name="begin_date", required=False, type=str),
        OpenApiParameter(name="end_date", required=False, type=str),
        OpenApiParameter(
            name="license_date_type",
            required=False,
            type=str,
            enum=["Creation", "Expiration"],
        ),
    ],
    responses={
        200: inline_serializer(
            name="All Businesses",
            fields={
                "begin_date": serializers.CharField(required=False),
                "end_date": serializers.CharField(required=False),
                "license_date_type": serializers.CharField(required=False),
            },
        ),
    },
)
@api_view(["GET"])
def business_list(request):
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
        OpenApiParameter(
            name="license_status",
            required=True,
            type=str,
            enum=["Active", "Inactive"],
        ),
        OpenApiParameter(
            name="license_date_type",
            required=False,
            type=str,
            enum=["Creation", "Expiration"],
        ),
        OpenApiParameter(name="begin_date", required=False, type=str),
        OpenApiParameter(name="end_date", required=False, type=str),
    ],
    responses={
        200: inline_serializer(
            name="Businesses License Status",
            fields={
                "license_status": serializers.CharField(),
                "begin_date": serializers.CharField(required=False),
                "end_date": serializers.CharField(required=False),
                "license_date_type": serializers.CharField(required=False),
            },
        ),
    },
)
@api_view(["GET"])
def business_license_status(request):
    filter_kwargs = {}
    filter_name = ""

    if (
        not request.GET.get("license_date_type")
        and not request.GET.get("begin_date")
        and not request.GET.get("end_date")
    ):
        license_status = request.GET.get("license_status")
        filter_kwargs["license_status"] = license_status
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

    license_status = request.GET.get("license_status")
    license_date_type = request.GET.get("license_date_type")
    start_date_str = request.GET.get("begin_date")
    end_date_str = request.GET.get("end_date")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    if license_date_type == "Creation":
        filter_name = "license_creation_date"
    else:
        filter_name = "lic_expir_dd"

    filter_kwargs["license_status"] = license_status
    filter_kwargs[f"{filter_name}__gte"] = start_date
    filter_kwargs[f"{filter_name}__lte"] = end_date

    instance = Business.objects.filter(**filter_kwargs)
    count_businesses = Business.objects.filter(**filter_kwargs).count()
    serializer = BusinessSerializer(instance, many=True)
    return Response(
        {"number_of_businesses": count_businesses, "businesses": serializer.data}
    )
