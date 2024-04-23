from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from tax_calculator.serializers import TaxCalculatorSerializer
from tax_calculator.utils import calculate_marginal_tax, get_tax_brackets


@api_view(['POST'])
def tax_calculator(request):
    serializer = TaxCalculatorSerializer(data=request.data)
    if serializer.is_valid():
        tax_year = serializer.validated_data['tax_year']

        try:
            dict_data = get_tax_brackets(tax_year)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if dict_data.get('errors'):
            return Response({'errors': dict_data['errors']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = calculate_marginal_tax(
            serializer.validated_data['annual_income'],
            tax_year, dict_data['tax_brackets'])
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
