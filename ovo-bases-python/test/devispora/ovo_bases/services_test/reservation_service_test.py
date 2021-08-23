import unittest

from devispora.ovo_bases.models.facility import Facility
from devispora.ovo_bases.models.incoming_request import IncomingRequest, RequestType
from devispora.ovo_bases.models.reservations import ReservationContext, ReservationType
from devispora.ovo_bases.models.helpers.reservation_helper import create_temp_reservations


class ReservationServiceTest(unittest.TestCase):

    def test_cast_reservations_succeed(self):
        """We're asserting here that the models map correctly, and it will break if (accidental) changes are made"""
        # Arrange
        start_time = 12456780
        end_time = 12456789
        group_name = 'Test'
        test_request = IncomingRequest(
            facilities=[Facility(2, 1, 'basename', 1, 'basetype')],
            reservation_type=ReservationType.Scrim,
            request_type=RequestType.Availability,
            start_time=start_time,
            end_time=end_time,
            group_name=group_name
        )
        # Act
        result = create_temp_reservations(test_request)
        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(group_name, result[0].group_name)
        self.assertEqual(ReservationType.Scrim, result[0].reservation_type)
        self.assertEqual(start_time, result[0].start_time)
        self.assertEqual(end_time, result[0].end_time)


if __name__ == '__main__':
    unittest.main()
