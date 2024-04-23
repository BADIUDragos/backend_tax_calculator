from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from tax_calculator.serializers import TaxCalculatorSerializer

from tax_calculator.utils.APIConnector import APIConnector, ServiceException
from tax_calculator.utils.utils import calculate_marginal_tax


# If I had more time I would also us IsAuthenticated to check for user authenticated by using the Auth app
@api_view(['POST'])
def tax_calculator(request):
    serializer = TaxCalculatorSerializer(data=request.data)
    if serializer.is_valid():
        tax_year = serializer.validated_data['tax_year']
        api_connector = APIConnector()
        url = f'http://localhost:5001/tax-calculator/tax-year/{tax_year}'

        # the idea here is to make the request to the backend API before doing anything else
        try:
            data = api_connector.make_request(url)
        except ServiceException as e:
            return Response(data=e.errors, status=e.status)

        result = calculate_marginal_tax(serializer.validated_data['annual_income'], data['tax_brackets'])

        return Response(result, status=status.HTTP_200_OK)

    # controlling cases of bad data sent to the endpoint, look at the TaxCalculatorSerializer for data validation
    else:
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
