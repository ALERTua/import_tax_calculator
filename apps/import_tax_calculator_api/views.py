from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImportUnitSerializer
try:
    from apps.import_tax_calculator.models import ImportUnit, Currency
except:
    from import_tax_calculator.models import ImportUnit, Currency


class ImportUnitModelAPIView(APIView):
    def get(self, request):
        serializer = ImportUnitSerializer(data=request.query_params)
        if serializer.is_valid():
            price = serializer.validated_data['price']
            currency = serializer.validated_data['currency']

            model = ImportUnit(price=price, currency=currency)
            tax = model.calculate_tax()
            return Response({'tax': tax, 'currency': currency})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
