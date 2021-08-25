import unittest

from devispora.ovo_bases.models.facility import Facility
from devispora.ovo_bases.models.helpers.reservation_helper import create_temp_reservations, \
    create_reservation_query_pool, create_query_dict
from devispora.ovo_bases.models.incoming_request import IncomingRequest, RequestType
from devispora.ovo_bases.models.reservations import ReservationType, Reservation, ReservationContinent
from devispora.ovo_bases.tools.time_service import one_hour_in_seconds


class ReservationHelperTest(unittest.TestCase):
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

    def test_create_query_dict(self):
        reservations = [
            Reservation(
                facility_id=3430,
                continent=ReservationContinent.Indar,
                start_time=2847000,
                end_time=2851200,
                group_name='Test',
                reservation_type=ReservationType.POG
            ),
            Reservation(
                facility_id=3430,
                continent=ReservationContinent.Indar,
                start_time=2851200,
                end_time=2861400,
                group_name='Test',
                reservation_type=ReservationType.POG
            ),
            Reservation(
                facility_id=266000,
                continent=ReservationContinent.Hossin,
                start_time=2851200,
                end_time=2861400,
                group_name='Test',
                reservation_type=ReservationType.POG
            )
        ]
        result = create_query_dict(reservations)
        self.assertEqual(1, len(result[2764800]))
        self.assertEqual(2, len(result[2851200]))

    def test_create_reservation_query_pool(self):
        reservations = [
            Reservation(
                facility_id=3430,
                continent=ReservationContinent.Indar,
                start_time=2847000,
                end_time=2851200,
                group_name='Test',
                reservation_type=ReservationType.POG
            ),
            Reservation(
                facility_id=3430,
                continent=ReservationContinent.Indar,
                start_time=2851200,
                end_time=2861400,
                group_name='Test',
                reservation_type=ReservationType.POG
            ),
            Reservation(
                facility_id=266000,
                continent=ReservationContinent.Hossin,
                start_time=2851200,
                end_time=2861400,
                group_name='Test',
                reservation_type=ReservationType.POG
            )
        ]
        result = create_reservation_query_pool(reservations)
        self.assertFalse(result[0].multi_continent)
        self.assertTrue(result[1].multi_continent)
        self.assertEqual(ReservationContinent.Indar, result[0].continent)
        self.assertEqual(ReservationContinent.Indar, result[0].continent)
        self.assertEqual(2764800, result[0].reservation_day)
        self.assertEqual(2851200, result[1].reservation_day)
