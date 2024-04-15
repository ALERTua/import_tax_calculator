from django.shortcuts import render
from django.http import JsonResponse
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


def health_check(request):
    """
    Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        JSONResponse: Returns a JSON response with the health status
    """
    return JsonResponse({'status': 'OK'})
