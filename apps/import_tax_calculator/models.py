"""Models for import_tax_calculator app."""

from copy import copy
from enum import Enum
from typing import ClassVar

from django.db import models


class Currency(Enum):
    """Enumeration of supported currencies."""

    EUR = "Euro"
    USD = "US Dollar"


class ImportUnit(models.Model):
    """Model representing an imported unit with price and currency information."""

    currency_choices: ClassVar[list[tuple[str, str]]] = [(_.name, _.value) for _ in Currency]

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    currency = models.CharField(
        max_length=3,
        choices=currency_choices,
        default=Currency.EUR,
        verbose_name=Currency.__class__.__name__,
    )

    def __str__(self) -> str:
        """Return string representation of the ImportUnit."""
        return f"{self.__class__.__name__}: {self.price} {self.currency}"

    def calculate_tax(self) -> float | None:
        """
        Calculate the customs tax for this import unit.

        Calculates duty and VAT based on the customs constants and exchange rates.
        Returns 0 if the price is at or below the customs limit.

        Returns:
            The total tax amount (duty + VAT) rounded to 1 decimal place,
            or None if customs constants or exchange rate are not configured.

        """
        customs_constants = CustomsConstants.objects.first()

        if not customs_constants:
            # Обробка випадку, коли константи ще не були встановлені
            return None

        exchange_rate = ExchangeRate.objects.first()
        if not exchange_rate:
            # Обробка випадку, коли константи ще не були встановлені
            return None

        price_euro = copy(self.price)
        if self.currency == "USD":
            price_euro = self.price / exchange_rate.euro_to_usd

        if price_euro <= customs_constants.limit:
            return 0

        excess = price_euro - customs_constants.limit
        duty = excess * customs_constants.duty_rate
        vat = (excess + duty) * customs_constants.vat_rate
        total_tax = duty + vat
        return round(float(total_tax), 1)


class CustomsConstants(models.Model):
    """Model representing customs constants (limit, duty rate, VAT rate)."""

    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=150,
        verbose_name="Limit for customs clearance",
    )
    duty_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.10, verbose_name="Duty rate")
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.20, verbose_name="VAT rate")

    def __str__(self) -> str:
        """Return string representation of the CustomsConstants."""
        return f"{self.__class__.__name__}"


class ExchangeRate(models.Model):
    """Model representing exchange rate (EUR to USD)."""

    euro_to_usd = models.DecimalField(max_digits=6, decimal_places=2, default=1.18)

    def __str__(self) -> str:
        """Return string representation of the ExchangeRate."""
        return f"Exchange Rate: 1 EURO = {self.euro_to_usd} USD"


if __name__ == "__main__":
    pass
