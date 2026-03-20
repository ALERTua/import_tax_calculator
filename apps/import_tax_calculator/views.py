"""Views for import_tax_calculator app."""

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView

from .forms import ImportUnitForm
from .models import ImportUnit


class CalculateCustomsView(FormView):
    """View for calculating customs tax for import units."""

    template_name = "calculate.html"
    form_class = ImportUnitForm

    def form_valid(self, form: ImportUnitForm) -> render:
        """
        Handle valid form submission and calculate tax.

        Args:
            form: The validated form instance.

        Returns:
            Rendered template with the form and calculated tax.

        """
        price = form.cleaned_data["price"]
        currency = form.cleaned_data["currency"]

        import_unit = ImportUnit(price=price, currency=currency)

        tax = import_unit.calculate_tax()

        return render(self.request, self.template_name, {"form": form, "tax": tax})


def health_check(_request: HttpRequest) -> JsonResponse:
    """
    Perform a Health Check.

    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).

    Args:
        request: The HTTP request object.

    Returns:
        JSONResponse: Returns a JSON response with the health status

    """
    return JsonResponse({"status": "OK"})
