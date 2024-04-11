from django.contrib import admin

from source.import_tax_calculator.models import CustomsConstants, ExchangeRate


# Register your models here.
@admin.register(CustomsConstants)
class CustomsConstantsAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    pass
