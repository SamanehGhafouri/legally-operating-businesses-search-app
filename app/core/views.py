from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from core.serializers import BusinessSerializer
from core.models import Business
from rest_framework import serializers
from datetime import datetime


@extend_schema(
    parameters=[
        OpenApiParameter(name="begin_date", required=False, type=str),
        OpenApiParameter(name="end_date", required=False, type=str),
    ],
    responses={
        200: inline_serializer(
            name="begin_date",
            fields={
                "begin_date": serializers.CharField(),
                "end_date": serializers.CharField(),
            },
        ),
    },
)
@api_view(["GET"])
def business_list(request):
    if request.GET.get("begin_date") is None and request.GET.get("end_date") is None:
        instance = Business.objects.all()
        serializer = BusinessSerializer(instance, many=True)
        return Response(serializer.data)
    else:
        filter_kwargs = {}
        start_date_str = request.GET.get("begin_date")
        end_date_str = request.GET.get("end_date")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if not start_date or not end_date:
            return Response({"error": "start_date parameter is required."}, status=400)

        filter_kwargs["license_creation_date__gte"] = start_date
        filter_kwargs["license_creation_date__lte"] = end_date
        instance = Business.objects.filter(**filter_kwargs)
        serializer = BusinessSerializer(instance, many=True)
        return Response({"businesses": serializer.data})


@extend_schema(
    summary="Get businesess by their license status",
    description="Get businesses by license status and range of creation dates",
    parameters=[
        OpenApiParameter(
            name="license_status",
            required=True,
            type=str,
            enum=["Active", "Inactive"],
        ),
        OpenApiParameter(name="begin_date", required=True, type=str),
        OpenApiParameter(name="end_date", required=True, type=str),
    ],
    responses={
        200: inline_serializer(
            name="License", fields={"license_status": serializers.CharField()}
        ),
    },
)
@api_view(["GET"])
def business_license_status(request):
    filter_kwargs = {}
    license_status = request.GET.get("license_status")
    start_date_str = request.GET.get("begin_date")
    end_date_str = request.GET.get("end_date")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    if license_status and start_date and end_date:
        filter_kwargs["license_status"] = license_status
        filter_kwargs["license_creation_date__gte"] = start_date
        filter_kwargs["license_creation_date__lte"] = end_date
    instance = Business.objects.filter(**filter_kwargs)
    serializer = BusinessSerializer(instance, many=True)
    return Response({"businesses": serializer.data})
