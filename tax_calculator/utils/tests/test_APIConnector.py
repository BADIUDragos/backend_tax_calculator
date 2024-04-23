import unittest
from unittest.mock import patch, Mock

import requests
from requests.exceptions import HTTPError

from tax_calculator.utils.APIConnector import APIConnector, ServiceException


class TestAPIConnector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://fakeurl.ca'

    @patch('requests.get')
    def test_make_request_success(self, mock_get):
        mock_response = Mock()
        expected_dict = {'success': True}
        mock_response.json.return_value = expected_dict
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        connector = APIConnector()
        response = connector.make_request(self.url)

        self.assertEqual(response, expected_dict)

    @patch('requests.get')
    def test_make_request_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        connector = APIConnector()

        with self.assertRaises(ServiceException) as context:
            connector.make_request(self.url)

        self.assertEqual(context.exception.status_code, 503)

    @patch('requests.get')
    def test_make_request_connection_error_retry(self, mock_get):
        mock_get.side_effect = [requests.ConnectionError("Connection failed"),
                                Mock(status_code=200, json=Mock(return_value={'success': True}))]

        connector = APIConnector(max_attempts=2)

        response = connector.make_request(self.url)

        self.assertEqual(response, {'success': True})
        self.assertEqual(mock_get.call_count, 2)

    @patch('requests.get')
    def test_make_request_http_error(self, mock_get):
        mock_response = Mock(status_code=400, json=lambda: {'errors': [{'message': 'Bad Request'}]})
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError(response=mock_response)

        connector = APIConnector()

        with self.assertRaises(ServiceException) as context:
            connector.make_request(self.url)

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn('Bad Request', str(context.exception.errors))

    @patch('requests.get')
    def test_on_database_not_found_retry(self, mock_get):
        error_response_mock = Mock()
        error_response_mock.json.return_value = {'errors': [{'message': 'Database not found!'}]}

        mock_get.side_effect = [HTTPError(response=error_response_mock),
                                Mock(status_code=200, json=Mock(return_value={'success': True}))]

        connector = APIConnector(max_attempts=2)

        response = connector.make_request(self.url)

        self.assertEqual(response, {'success': True})
        self.assertEqual(mock_get.call_count, 2)

    @patch('requests.get')
    def test_make_request_timeout_error(self, mock_get):
        mock_get.side_effect = requests.Timeout("Request timed out")

        connector = APIConnector()

        with self.assertRaises(ServiceException) as context:
            connector.make_request(self.url)

        self.assertEqual(context.exception.status_code, 504)
        self.assertIn('TIMEOUT', str(context.exception.errors))
