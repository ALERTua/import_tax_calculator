"""Models for import_tax_calculator app."""

from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import ClassVar

from django.db import models


class CustomsConfigError(RuntimeError):
    """Raised when customs constants or exchange rate are not configured."""


class Currency(Enum):
    """Enumeration of supported currencies."""

    EUR = "Euro"
    USD = "US Dollar"


class SingletonModel(models.Model):
    """Abstract base that pins primary key to 1 so only one row can ever exist."""

    class Meta:
        """Meta options."""

        abstract = True

    def save(self, *args: object, **kwargs: object) -> None:
        """Force pk=1 so save always upserts the singleton row."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> SingletonModel:
        """Return the singleton instance, creating it with defaults if absent."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ImportUnit(models.Model):
    """Model representing an imported unit with price and currency information."""

    currency_choices: ClassVar[list[tuple[str, str]]] = [(_.name, _.value) for _ in Currency]

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    currency = models.CharField(
        max_length=3,
        choices=currency_choices,
        default=Currency.EUR.name,
        verbose_name="Currency",
    )

    class Meta:
        """Meta options for ImportUnit model."""

        app_label = "import_tax_calculator"

    def __str__(self) -> str:
        """Return string representation of the ImportUnit."""
        return f"{self.__class__.__name__}: {self.price} {self.currency}"

    def calculate_tax(self) -> Decimal:
        """
        Calculate the customs tax for this import unit.

        Returns 0 if the price is at or below the customs limit.

        Raises:
            CustomsConfigError: If CustomsConstants or ExchangeRate are not configured.

        """
        customs_constants = CustomsConstants.objects.first()
        if not customs_constants:
            msg = "CustomsConstants is not configured"
            raise CustomsConfigError(msg)

        exchange_rate = ExchangeRate.objects.first()
        if not exchange_rate:
            msg = "ExchangeRate is not configured"
            raise CustomsConfigError(msg)

        price_euro = self.price
        if self.currency == Currency.USD.name:
            price_euro = self.price / exchange_rate.euro_to_usd

        if price_euro <= customs_constants.limit:
            return Decimal(0)

        excess = price_euro - customs_constants.limit
        duty = excess * customs_constants.duty_rate
        vat = (excess + duty) * customs_constants.vat_rate
        total_tax_eur = duty + vat

        # Return the tax in the same currency the caller used, so the label matches the price
        total_tax = total_tax_eur
        if self.currency == Currency.USD.name:
            total_tax = total_tax_eur * exchange_rate.euro_to_usd

        return total_tax.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


class CustomsConstants(SingletonModel):
    """Singleton row holding customs constants (limit, duty rate, VAT rate)."""

    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=150,
        verbose_name="Limit for customs clearance",
    )
    duty_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.10, verbose_name="Duty rate")
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.20, verbose_name="VAT rate")

    class Meta:
        """Meta options for CustomsConstants model."""

        app_label = "import_tax_calculator"

    def __str__(self) -> str:
        """Return string representation of the CustomsConstants."""
        return f"{self.__class__.__name__}"


class ExchangeRate(SingletonModel):
    """Singleton row holding the EUR to USD exchange rate."""

    euro_to_usd = models.DecimalField(max_digits=6, decimal_places=2, default=1.18)

    class Meta:
        """Meta options for ExchangeRate model."""

        app_label = "import_tax_calculator"

    def __str__(self) -> str:
        """Return string representation of the ExchangeRate."""
        return f"Exchange Rate: 1 EURO = {self.euro_to_usd} USD"
