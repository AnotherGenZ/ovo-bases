import os
import unittest

from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.helpers.incoming_request_helper import parse_incoming_request, retrieve_request_type, \
    discover_request, retrieve_and_convert_time
from devispora.ovo_bases.models.incoming_request import RequestType
from devispora.ovo_bases.models.reservations import ReservationType, ReservationContext


class IncomingRequestHelperTest(unittest.TestCase):
    def test_parse_incoming_request_pog_succeed(self):
        incoming_request = {
            'facility_ids': [266000, 239000],
            'reservation_type': 'pog',
            'request_type': 'availability',
            'group_name': 'POG_BOT'
        }
        os.environ['MAP_REGION_LOCATION'] = '../../../../resources/map_region.json'
        parser = BaseParser()
        # Act
        parser.create_base_list()
        result = parse_incoming_request(parser, incoming_request)
        # Assert
        self.assertEqual(ReservationType.POG, result.reservation_type)
        self.assertEqual(RequestType.Availability, result.request_type)
        self.assertEqual(266000, result.facilities[0].facility_id)
        self.assertEqual(239000, result.facilities[1].facility_id)
        self.assertEqual('POG_BOT', result.group_name)

    def test_retrieve_request_type_wrong(self):
        request_type_string = 'DoesNotExist'
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.RequestTypeNotRecognised,
            retrieve_request_type, request=request_type_string
        )

    def test_retrieve_request_type_found(self):
        request_type_string = 'reservation'
        result = retrieve_request_type(request_type_string)
        self.assertEqual(RequestType.Reservation, result)

    def test_discover_request_misses_key(self):
        incoming_request = {
            'base_ids': [266000, 239000],
            'reservation_type': 'pog',
            'group_name': 'POG_BOT'
        }
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.RequestTypeNotProvided,
            discover_request, raw_body=incoming_request
        )

    def test_discover_request_contains_key(self):
        incoming_request = {
            'base_ids': [266000, 239000],
            'reservation_type': 'pog',
            'request_type': 'availability',
            'group_name': 'POG_BOT'
        }
        result = discover_request(incoming_request)
        self.assertEqual(RequestType.Availability, result)

    def test_discover_request_contains_wrong_type(self):
        incoming_request = {
            'base_ids': [266000, 239000],
            'reservation_type': 'pog',
            'request_type': 'WrongType',
            'group_name': 'POG_BOT'
        }
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.RequestTypeNotRecognised,
            discover_request, raw_body=incoming_request
        )

    def test_retrieve_and_convert_time_not_int(self):
        not_int = 'text'
        context = ReservationContext.EndTime
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.IntValueError,
            retrieve_and_convert_time, raw_time=not_int, context=context
        )

    def test_retrieve_and_convert_time_works(self):
        not_int = '123'
        context = ReservationContext.EndTime
        result = retrieve_and_convert_time(not_int, context)
        self.assertEqual(int(not_int), result)


if __name__ == '__main__':
    unittest.main()
