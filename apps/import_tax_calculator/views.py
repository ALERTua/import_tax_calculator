from django.shortcuts import render
from django.views.generic import FormView
from .models import ImportUnit
from .forms import ImportUnitForm


class CalculateCustomsView(FormView):
    template_name = 'calculate.html'
    form_class = ImportUnitForm

    def form_valid(self, form):
        price = form.cleaned_data['price']
        currency = form.cleaned_data['currency']

        import_unit = ImportUnit(price=price, currency=currency)
        # import_unit.save()

        tax = import_unit.calculate_tax()

        return render(self.request, self.template_name, {'form': form, 'tax': tax})
