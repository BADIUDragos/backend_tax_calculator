import time

import requests
import logging

logger = logging.getLogger('tax_calculator')


def get_tax_brackets(tax_year):
    url = f'http://localhost:5001/tax-calculator/tax-year/{tax_year}'
    retries = 5

    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error on attempt {attempt + 1}: {http_err}')
        except Exception as err:
            logger.error(f'Other error on attempt {attempt + 1}: {err}')

        if attempt < retries:
            time.sleep(2)

    error_message = "All attempts to fetch tax brackets have failed. Please try submitting a request again."
    logger.error(error_message)
    return {"error": error_message}


def calculate_marginal_tax(annual_income, tax_year):

    brackets = get_tax_brackets(tax_year)

    taxes_owed_per_band = []
    total_taxes = 0

    for bracket in brackets['tax_brackets']:
        lower_bound = bracket['min']
        rate = bracket['rate']
        upper_bound = bracket.get('max', float('inf'))
        if annual_income > lower_bound:
            upper_bound = min(annual_income, upper_bound)
            income_in_bracket = upper_bound - lower_bound
            tax_for_bracket = round(income_in_bracket * rate, 4)
            taxes_owed_per_band.append((rate, tax_for_bracket))
            total_taxes += tax_for_bracket

    effective_tax_rate = round(total_taxes / annual_income, 4)

    return {
        'total_taxes': total_taxes,
        'taxes_owed_per_band': taxes_owed_per_band,
        'effective_tax_rate': effective_tax_rate
    }

