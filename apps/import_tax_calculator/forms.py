from django import forms
from .models import ImportUnit, Currency


class ImportUnitForm(forms.ModelForm):
    class Meta:
        model = ImportUnit
        fields = ['price', 'currency']
        labels = {
            'price': 'Price',
            'currency': 'Currency',
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")

        return price

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if currency:
            currency = currency.upper()
        if currency not in (currencies := [_.name for _ in Currency]):
            raise forms.ValidationError(f"Currency must be among supported currencies: {currencies}")

        return currency
