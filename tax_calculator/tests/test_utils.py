import unittest

import requests
import requests_mock
from tax_calculator.utils import get_tax_brackets


class GetTaxBracketsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.year = 2022
        cls.url = f'http://localhost:5001/tax-calculator/tax-year/2022'
        cls.mock_brackets_response = {
            'tax_brackets': [{"rate": 0.0, "min": 0, "max": 30000}, {"rate": 0.1, "min": 30000, "max": 50000},
                             {"rate": 0.2, "min": 50000}]
        }

        cls.mock_url_not_found_error = {"errors": [{"code": "NOT_FOUND", "field": "", "message": "That url was not found"}]}
        cls.random_error_it_throws = {"errors": [{"code": "INTERNAL_SERVER_ERROR", "field": "", "message": "Database not found!"}]}
        cls.timeout_error_message = "All attempts to fetch tax brackets have failed. Please try submitting a request again."

    @requests_mock.Mocker()
    def test_get_tax_brackets_success(self, m):
        m.get(f'http://localhost:5001/tax-calculator/tax-year/{self.year}', json=self.mock_brackets_response)

        data = get_tax_brackets(self.year)
        self.assertEqual(data, self.mock_brackets_response)

    @requests_mock.Mocker()
    def test_get_tax_brackets_not_found_error(self, m):
        m.get(f'http://localhost:5001/tax-calculator/tax-year/{self.year}', json=self.mock_url_not_found_error, status_code=404)
        data = get_tax_brackets(self.year)
        self.assertEqual(data, self.mock_url_not_found_error)

    @requests_mock.Mocker()
    def test_get_tax_brackets_timeout(self, m):
        m.get(self.url, exc=requests.exceptions.Timeout)
        data = get_tax_brackets(self.year)
        self.assertEqual(data[0]['error'], self.timeout_error_message)
        self.assertEqual(data[1], 500)
