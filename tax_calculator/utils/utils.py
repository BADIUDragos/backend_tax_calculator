import logging


logger = logging.getLogger('tax_calculator')


def calculate_marginal_tax(annual_income, brackets):

    taxes_owed_per_band = []
    total_taxes = 0

    for bracket in brackets:
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

