import unittest

from devispora.ovo_bases.exception.exceptions import RequestExceptionMessage, RequestException
from devispora.ovo_bases.services.request_service import discover_request, RequestType, retrieve_request_type


class RequestServiceTest(unittest.TestCase):

    def test_retrieve_request_type_wrong(self):
        request_type_string = 'DoesNotExist'
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.RequestTypeNotRecognised,
            retrieve_request_type, request=request_type_string
        )

    def test_retrieve_request_type_found(self):
        request_type_string = 'Reservation'
        result = retrieve_request_type(request_type_string)
        self.assertEqual(RequestType.Reservation, result)

    def test_discover_request_misses_key(self):
        incoming_request = {
            'base_ids': [266000, 239000],
            'event_type': 'POG',
            'group_name': 'POG_BOT'
        }
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.RequestTypeNotProvided,
            discover_request, raw_body=incoming_request
        )

    def test_discover_request_contains_key(self):
        incoming_request = {
            'base_ids': [266000, 239000],
            'event_type': 'POG',
            'request_type': 'Availability',
            'group_name': 'POG_BOT'
        }
        result = discover_request(incoming_request)
        self.assertEqual(RequestType.Availability, result)

    def test_discover_request_contains_wrong_type(self):
        incoming_request = {
            'base_ids': [266000, 239000],
            'event_type': 'POG',
            'request_type': 'WrongType',
            'group_name': 'POG_BOT'
        }
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.RequestTypeNotRecognised,
            discover_request, raw_body=incoming_request
        )
