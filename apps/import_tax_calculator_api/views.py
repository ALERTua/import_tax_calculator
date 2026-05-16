"""Views for import_tax_calculator_api app."""

from typing import TYPE_CHECKING

from django.utils.cache import patch_cache_control
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.import_tax_calculator.models import CustomsConfigError, ImportUnit

from .serializers import ImportUnitSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest


class ImportUnitModelAPIView(APIView):
    """API view for ImportUnit model operations."""

    serializer_class = ImportUnitSerializer

    @extend_schema(
        parameters=[ImportUnitSerializer],
        responses={
            200: ImportUnitSerializer,
            400: OpenApiResponse(description="Validation error"),
            503: OpenApiResponse(description="Backend constants not configured"),
        },
    )
    def get(self, request: HttpRequest) -> Response:
        """Calculate import tax for the given price + currency query params."""
        serializer = ImportUnitSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        price = serializer.validated_data["price"]
        currency = serializer.validated_data["currency"]

        try:
            tax = ImportUnit(price=price, currency=currency).calculate_tax()
        except CustomsConfigError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        response = Response({"tax": tax, "currency": currency})
        # Pure function of (price, currency) + rarely-changing admin config.
        # Stale results self-recover within max_age.
        patch_cache_control(response, public=True, max_age=60)
        return response
