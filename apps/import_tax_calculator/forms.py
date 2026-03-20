"""Forms for import_tax_calculator app."""

from typing import ClassVar

from django import forms

from .models import Currency, ImportUnit


class ImportUnitForm(forms.ModelForm):
    """Form for creating and updating ImportUnit instances."""

    class Meta:
        """Meta configuration for ImportUnitForm."""

        model = ImportUnit
        fields = ("price", "currency")
        labels: ClassVar[dict[str, str]] = {
            "price": "Price",
            "currency": "Currency",
        }

    def clean_price(self) -> float:
        """
        Validate that the price is greater than zero.

        Returns:
            The validated price value.

        Raises:
            ValidationError: If price is less than or equal to zero.

        """
        price = self.cleaned_data["price"]
        if price <= 0:
            msg = "Price must be greater than zero."
            raise forms.ValidationError(msg)

        return price

    def clean_currency(self) -> str:
        """
        Validate and normalize the currency value.

        Returns:
            The normalized currency code in uppercase.

        Raises:
            ValidationError: If currency is not supported.

        """
        currency = self.cleaned_data["currency"]
        if currency:
            currency = currency.upper()
        if currency not in (currencies := [_.name for _ in Currency]):
            msg = f"Currency must be among supported currencies: {currencies}"
            raise forms.ValidationError(msg)

        return currency
