"""Views for import_tax_calculator_api app."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ImportUnitSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest

try:
    from apps.import_tax_calculator.models import ImportUnit
except ImportError:
    from import_tax_calculator.models import ImportUnit


class ImportUnitModelAPIView(APIView):
    """API view for ImportUnit model operations."""

    def get(self, request: HttpRequest) -> Response:
        """
        Handle GET requests to calculate tax for import unit.

        Args:
            request: The HTTP request object containing query parameters.

        Returns:
            Response: JSON response with calculated tax and currency.

        """
        serializer = ImportUnitSerializer(data=request.query_params)
        if serializer.is_valid():
            price = serializer.validated_data["price"]
            currency = serializer.validated_data["currency"]

            model = ImportUnit(price=price, currency=currency)
            tax = model.calculate_tax()
            return Response({"tax": tax, "currency": currency})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
