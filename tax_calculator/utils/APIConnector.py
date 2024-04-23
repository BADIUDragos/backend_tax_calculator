import requests
import logging
from requests.exceptions import HTTPError, Timeout, ConnectionError
from rest_framework import status


class ServiceException(Exception):
    def __init__(self, errors, status_code):
        self.errors = errors
        self.status_code = status_code
        super().__init__(self.errors)


class APIConnector:
    def __init__(self, max_attempts=5, timeout_seconds=10):
        self.max_attempts = max_attempts
        self.timeout_seconds = timeout_seconds
        self.logger = logging.getLogger('TaxAPIConnector')

    def make_request(self, url, attempt=1, **kwargs):
        try:
            response = requests.get(url, timeout=self.timeout_seconds, **kwargs)
            response.raise_for_status()
            return response.json()

        except ConnectionError as e:
            if attempt < self.max_attempts:
                self.logger.info(f'Retrying request (attempt {attempt + 1})')
                return self.make_request(url, attempt + 1, **kwargs)
            else:
                self.logger.error(f'Connection error on final attempt {attempt}: {str(e)}')
                error_response = {
                    'errors': [{'code': 'SERVICE_UNAVAILABLE', 'message': 'The API backend is not online.'}]
                }
                raise ServiceException(error_response, status.HTTP_503_SERVICE_UNAVAILABLE)

        except HTTPError as e:
            error_response = e.response.json()
            errors = error_response.get('errors', [])
            self.logger.error(f'HTTP error on attempt {attempt} : {errors}')

            if any(error.get('message') == 'Database not found!' for error in errors) and attempt < self.max_attempts:
                self.logger.info(f'Retrying request (attempt {attempt + 1})')
                return self.make_request(url, attempt + 1, **kwargs)

            raise ServiceException(errors, status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Timeout as e:
            self.logger.error(f'Timeout occurred on attempt {attempt}: {str(e)}')
            error_response = {
                'errors': [{'code': 'TIMEOUT', 'message': 'The request to the API backend timed out.'}]
            }
            raise ServiceException(error_response, status.HTTP_504_GATEWAY_TIMEOUT)
