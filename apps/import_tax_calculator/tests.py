"""Tests for import_tax_calculator models."""

from decimal import Decimal

import pytest
from django.test import TestCase

from .models import CustomsConfigError, CustomsConstants, ExchangeRate, ImportUnit

TOLERANCE = Decimal("0.01")


class ImportUnitTaxCalculationTestCase(TestCase):
    """Test case for import unit tax calculation."""

    def setUp(self) -> None:
        """Set up test data for each test method."""
        self.customs_constants = CustomsConstants.objects.create(
            limit=Decimal(150),
            duty_rate=Decimal("0.10"),
            vat_rate=Decimal("0.20"),
        )
        self.exchange_rate = ExchangeRate.objects.create(euro_to_usd=Decimal("1.18"))

    def test_tax_calculation_price_below_limit(self) -> None:
        """Test tax calculation when price is below the customs limit."""
        invoice = ImportUnit.objects.create(price=Decimal(100), currency="EUR")
        assert invoice.calculate_tax() == Decimal(0)

    def test_tax_calculation_price_equal_limit(self) -> None:
        """Test tax calculation when price equals the customs limit."""
        invoice = ImportUnit.objects.create(price=Decimal(150), currency="EUR")
        assert invoice.calculate_tax() == Decimal(0)

    def test_tax_calculation_price_above_limit(self) -> None:
        """Test tax calculation when price is above the customs limit."""
        invoice = ImportUnit.objects.create(price=Decimal(170), currency="EUR")
        tax = invoice.calculate_tax()
        assert abs(tax - Decimal("6.4")) < TOLERANCE

    def test_tax_in_usd_returned_in_usd(self) -> None:
        """USD input → tax returned in USD (computed via EUR conversion then converted back)."""
        invoice = ImportUnit.objects.create(price=Decimal(200), currency="USD")
        # price_eur=169.49, excess=19.49, duty=1.949, vat=4.288, tax_eur=6.237,
        # tax_usd=6.237*1.18=7.36 → quantize to 0.1 → 7.4
        tax = invoice.calculate_tax()
        assert abs(tax - Decimal("7.4")) < TOLERANCE

    def test_missing_constants_raises(self) -> None:
        """Test that missing customs constants raises CustomsConfigError."""
        CustomsConstants.objects.all().delete()
        invoice = ImportUnit.objects.create(price=Decimal(170), currency="EUR")
        with pytest.raises(CustomsConfigError):
            invoice.calculate_tax()
