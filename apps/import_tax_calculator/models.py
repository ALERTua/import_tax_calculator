from copy import copy
from enum import Enum
from django.db import models


class Currency(Enum):
    EUR = 'Euro'
    USD = 'US Dollar'


class ImportUnit(models.Model):
    currency_choices = [(_.name, _.value) for _ in Currency]

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    currency = models.CharField(max_length=3, choices=currency_choices, default=Currency.EUR,
                                verbose_name=Currency.__class__.__name__)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.price} {self.currency}"

    def calculate_tax(self):
        customs_constants = CustomsConstants.objects.first()

        if not customs_constants:
            # Обробка випадку, коли константи ще не були встановлені
            return None

        exchange_rate = ExchangeRate.objects.first()
        if not exchange_rate:
            # Обробка випадку, коли константи ще не були встановлені
            return None

        price_euro = copy(self.price)
        if self.currency == 'USD':
            price_euro = self.price / exchange_rate.euro_to_usd

        if price_euro <= customs_constants.limit:
            return 0

        excess = price_euro - customs_constants.limit
        duty = excess * customs_constants.duty_rate
        vat = (excess + duty) * customs_constants.vat_rate
        total_tax = duty + vat
        output = round(float(total_tax), 1)
        return output


class CustomsConstants(models.Model):
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=150, verbose_name='Limit for customs clearance')
    duty_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.10, verbose_name='Duty rate')
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.20, verbose_name='VAT rate')

    def __str__(self):
        return f"{self.__class__.__name__}"


class ExchangeRate(models.Model):
    euro_to_usd = models.DecimalField(max_digits=6, decimal_places=2, default=1.18)

    def __str__(self):
        return f"Exchange Rate: 1 EURO = {self.euro_to_usd} USD"


if __name__ == '__main__':
    pass
