"""Tests for import_tax_calculator_api app."""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.import_tax_calculator.models import CustomsConstants, ExchangeRate


class ImportUnitModelAPIViewTests(TestCase):
    """Cover the 200, 400, and 503 paths of the calculate_api endpoint."""

    url = reverse("calculate_import_tax_api")

    def setUp(self) -> None:
        """Provision the singleton config rows the calculation depends on."""
        self.client = APIClient()
        CustomsConstants.objects.create(
            limit=Decimal(150),
            duty_rate=Decimal("0.10"),
            vat_rate=Decimal("0.20"),
        )
        ExchangeRate.objects.create(euro_to_usd=Decimal("1.18"))

    def test_get_returns_tax(self) -> None:
        """Happy path: valid params → 200 with tax + currency."""
        response = self.client.get(self.url, {"price": "170", "currency": "EUR"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["currency"] == "EUR"
        assert abs(Decimal(str(response.data["tax"])) - Decimal("6.4")) < Decimal("0.01")

    def test_get_response_is_cacheable(self) -> None:
        """200 responses carry a Cache-Control max-age so browsers/CDNs can cache."""
        response = self.client.get(self.url, {"price": "170", "currency": "EUR"})
        assert "max-age=60" in response["Cache-Control"]

    def test_invalid_price_returns_400(self) -> None:
        """Non-numeric price fails serializer validation → 400."""
        response = self.client.get(self.url, {"price": "abc", "currency": "EUR"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "price" in response.data

    def test_missing_config_returns_503(self) -> None:
        """When backend constants are unset, calculate_tax raises → 503."""
        CustomsConstants.objects.all().delete()
        response = self.client.get(self.url, {"price": "170", "currency": "EUR"})
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "error" in response.data
