"""Tests for import_tax_calculator models."""

from django.test import TestCase

from .models import CustomsConstants, ImportUnit

TOLERANCE = 0.01


class ImportUnitTaxCalculationTestCase(TestCase):
    """Test case for import unit tax calculation."""

    def setUp(self) -> None:
        """Set up test data for each test method."""
        # Створення констант в адмінці
        self.customs_constants = CustomsConstants.objects.create(limit=150, duty_rate=0.10, vat_rate=0.20)

    def test_tax_calculation_price_below_limit(self) -> None:
        """Test tax calculation when price is below the customs limit."""
        invoice = ImportUnit.objects.create(price=100, currency="EUR")
        tax = invoice.calculate_tax()
        assert tax == 0, "Tax should be 0 for price at or below limit"

    def test_tax_calculation_price_equal_limit(self) -> None:
        """Test tax calculation when price equals the customs limit."""
        invoice = ImportUnit.objects.create(price=150, currency="EUR")
        tax = invoice.calculate_tax()
        assert tax == 0, "Tax should be 0 for price at or below limit"

    def test_tax_calculation_price_above_limit(self) -> None:
        """Test tax calculation when price is above the customs limit."""
        invoice = ImportUnit.objects.create(price=170, currency="EUR")
        tax = invoice.calculate_tax()
        assert abs(tax - 6.4) < TOLERANCE, "Tax should be approximately 6.4 for price above limit"
