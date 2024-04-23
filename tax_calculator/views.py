from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from tax_calculator.serializers import TaxCalculatorSerializer
from tax_calculator.utils import calculate_marginal_tax


@api_view(['POST'])
def tax_calculator(request):
    serializer = TaxCalculatorSerializer(data=request.data)
    if serializer.is_valid():
        try:
            result = calculate_marginal_tax(
                serializer.validated_data['annual_income'],
                serializer.validated_data['tax_year']
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
