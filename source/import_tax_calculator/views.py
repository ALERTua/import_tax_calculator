from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from .models import ImportUnit
from .forms import ImportUnitForm


class CalculateCustomsView(FormView):
    template_name = 'templates/calculate.html'
    form_class = ImportUnitForm

    def form_valid(self, form):
        price = form.cleaned_data['price']
        currency = form.cleaned_data['currency']

        # Отримання об'єкта ImportUnit з бази даних
        import_unit = ImportUnit(price=price, currency=currency)
        import_unit.save()

        # Розрахунок митних платежів
        tax = import_unit.calculate_tax()

        # Додавання результату розрахунку до контексту шаблону
        return render(self.request, self.template_name, {'form': form, 'tax': tax})
