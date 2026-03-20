"""Serializers for import_tax_calculator_api app."""

from decimal import Decimal

from rest_framework.serializers import ChoiceField, DecimalField, Serializer

from ..import_tax_calculator.models import Currency


class ImportUnitSerializer(Serializer):
    """Serializer for ImportUnit model."""

    price = DecimalField(
        max_digits=10,
        decimal_places=2,
        max_value=Decimal(999999),
        min_value=Decimal(-999999),
    )
    currency = ChoiceField(
        choices=[_.name for _ in Currency],
        required=False,
        default=Currency.EUR.name,
        initial=Currency.EUR.name,
        help_text=f"Currency among {[_.name for _ in Currency]}",
    )
