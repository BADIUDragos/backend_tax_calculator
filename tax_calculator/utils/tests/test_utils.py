import unittest

from tax_calculator.utils.utils import calculate_marginal_tax


class TestCalculateMarginalTax(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_brackets = [
            {"min": 0, "max": 20000, "rate": 0.0},
            {"min": 20000, "max": 40000, "rate": 0.1},
            {"min": 40000, "max": 60000, "rate": 0.2},
            {"min": 60000, "max": 80000, "rate": 0.3},
            {"min": 80000, "rate": 0.4}
        ]

        cls.expected_result_first_band_income = {'effective_tax_rate': 0.0,
                                                 'taxes_owed_per_band': [(0.0, 0.0)],
                                                 'total_taxes': 0.0}

        cls.expected_result_30000_income = {'effective_tax_rate': 0.0333,
                                            'taxes_owed_per_band': [(0.0, 0.0), (0.1, 1000.0)],
                                            'total_taxes': 1000.0}

        cls.expected_result_float_income = {'effective_tax_rate': 0.0333,
                                            'taxes_owed_per_band': [(0.0, 0.0), (0.1, 1000.045)],
                                            'total_taxes': 1000.045}

        cls.expected_result_last_band_income = {'effective_tax_rate': 0.2,
                                                'taxes_owed_per_band': [(0.0, 0.0),
                                                                        (0.1, 2000.0),
                                                                        (0.2, 4000.0),
                                                                        (0.3, 6000.0),
                                                                        (0.4, 8000.0)],
                                                'total_taxes': 20000.0}

    def test_calculate_marginal_tax_single_band(self):
        result = calculate_marginal_tax(15000, self.mock_brackets)
        self.assertEqual(result, self.expected_result_first_band_income)

    def test_calculate_marginal_tax_income_equals_bracket_upper_bound(self):
        result = calculate_marginal_tax(20000, self.mock_brackets)
        self.assertEqual(result, self.expected_result_first_band_income)

    def test_calculate_marginal_tax_income_middle_second_band(self):
        result = calculate_marginal_tax(30000, self.mock_brackets)
        self.assertEqual(result, self.expected_result_30000_income)

    def test_calculate_marginal_tax_income_float(self):
        result = calculate_marginal_tax(30000.45, self.mock_brackets)
        self.assertEqual(result, self.expected_result_float_income)

    def test_calculate_marginal_tax_income_no_max_band(self):
        result = calculate_marginal_tax(100000, self.mock_brackets)
        self.assertEqual(result, self.expected_result_last_band_income)
