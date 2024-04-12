from django.contrib import admin

from .models import CustomsConstants, ExchangeRate


# Register your models here.
@admin.register(CustomsConstants)
class CustomsConstantsAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    pass
