"""Views for import_tax_calculator app."""

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView

from .forms import ImportUnitForm
from .models import CustomsConfigError, ImportUnit


class CalculateCustomsView(FormView):
    """View for calculating customs tax for import units."""

    template_name = "calculate.html"
    form_class = ImportUnitForm

    def form_valid(self, form: ImportUnitForm) -> render:
        """Handle valid form submission and calculate tax."""
        import_unit = ImportUnit(
            price=form.cleaned_data["price"],
            currency=form.cleaned_data["currency"],
        )
        try:
            tax = import_unit.calculate_tax()
        except CustomsConfigError as exc:
            form.add_error(None, f"Service unavailable: {exc}")
            return self.form_invalid(form)

        return render(self.request, self.template_name, {"form": form, "tax": tax})


def health_check(_request: HttpRequest) -> JsonResponse:
    """Return a 200 JSON response so orchestrators can probe container health."""
    return JsonResponse({"status": "OK"})
