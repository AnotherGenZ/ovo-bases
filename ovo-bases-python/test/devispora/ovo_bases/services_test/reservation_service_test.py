import json
import os
import unittest

from devispora.ovo_bases.bases.parse_bases import BasesParser
from devispora.ovo_bases.exception.exceptions import ReservationException, ReservationExceptionMessage
from devispora.ovo_bases.models.reservations import ReservationContext
from devispora.ovo_bases.services.reservation_service import create_temp_reservation


class ReservationServiceTest(unittest.TestCase):

    def test_cast_reservation_succeed(self):
        test_body = {
            ReservationContext.BaseID.value: 266000,
            ReservationContext.EventType.value: 'scrim',
            ReservationContext.GroupName.value: 'Test',
            ReservationContext.StartTime.value: 12456789,
            ReservationContext.EndTime.value: 12456780
        }
        json_body = json.loads(json.dumps(test_body))
        result = create_temp_reservation(create_base_list(), json_body)
        self.assertEqual('Test', result.group_name)

    def test_cast_reservation_missing(self):
        empty_body = {}
        self.assertRaisesRegex(
            ReservationException, ReservationExceptionMessage.MissingReservationPart,
            create_temp_reservation, base_list=create_base_list(), raw_reservation=empty_body
        )


def create_base_list():
    os.environ['MAP_REGION_LOCATION'] = '../../../resources/map_region.json'
    return BasesParser().create_base_list()


if __name__ == '__main__':
    unittest.main()