"""Views for import_tax_calculator_api app."""

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.import_tax_calculator.models import CustomsConfigError, ImportUnit

from .serializers import ImportUnitSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest


class ImportUnitModelAPIView(APIView):
    """API view for ImportUnit model operations."""

    def post(self, request: HttpRequest) -> Response:
        """Calculate import tax for the posted ImportUnit payload."""
        serializer = ImportUnitSerializer(data=request.data)
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

        return Response({"tax": tax, "currency": currency})
