"""Admin configuration for import_tax_calculator models."""

from django.contrib import admin

from .models import CustomsConstants, ExchangeRate


@admin.register(CustomsConstants)
class CustomsConstantsAdmin(admin.ModelAdmin):
    """Admin interface for CustomsConstants model."""


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    """Admin interface for ExchangeRate model."""
