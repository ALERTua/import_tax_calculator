from django.test import TestCase
from .models import CustomsConstants, ImportUnit


class ImportUnitTaxCalculationTestCase(TestCase):
    def setUp(self):
        # Створення констант в адмінці
        self.customs_constants = CustomsConstants.objects.create(limit=150, duty_rate=0.10, vat_rate=0.20)

    def test_tax_calculation_price_below_limit(self):
        invoice = ImportUnit.objects.create(price=100, currency='EUR')
        tax = invoice.calculate_tax()
        self.assertEqual(tax, 0)

    def test_tax_calculation_price_equal_limit(self):
        invoice = ImportUnit.objects.create(price=150, currency='EUR')
        tax = invoice.calculate_tax()
        self.assertEqual(tax, 0)

    def test_tax_calculation_price_above_limit(self):
        invoice = ImportUnit.objects.create(price=170, currency='EUR')
        tax = invoice.calculate_tax()
        self.assertAlmostEqual(tax, 6.4, places=2)
