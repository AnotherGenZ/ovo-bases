import json
import unittest

from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.responses import error_response


class ResponsesTest(unittest.TestCase):
    def test_error_response(self):
        rex = RequestException(RequestExceptionMessage.RequestTypeNotProvided)
        result = json.dumps(error_response(rex))
        self.assertEqual(
            '{"RequestTypeNotProvided": "A request type must be provided"}',
            json.loads(result)['body']
        )
