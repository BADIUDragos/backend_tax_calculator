from rest_framework import serializers


class TaxCalculatorSerializer(serializers.Serializer):
    annual_income = serializers.FloatField(min_value=0.01, error_messages={"min_value": "annual_income must be positive"})
    tax_year = serializers.IntegerField(min_value=2019, max_value=2023, error_messages={
        "min_value": "tax_year must be at least 2019",
        "max_value": "tax_year must be no later than 2023"
    })
