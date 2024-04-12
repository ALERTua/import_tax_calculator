from django import forms
from .models import ImportUnit


class ImportUnitForm(forms.ModelForm):
    class Meta:
        model = ImportUnit
        fields = ['price', 'currency']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")

        return price
