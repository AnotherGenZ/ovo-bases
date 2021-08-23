import unittest
from decimal import Decimal

from devispora.ovo_bases.models.helpers.reservation_helper import create_reservations_list, reservation_splitter
from devispora.ovo_bases.models.reservations import ReservationType, ReservationContinent, Reservation
from devispora.ovo_bases.tools.time_service import day_in_seconds, get_event_day_from_timestamp


class ReservationHelperTest(unittest.TestCase):
    def test_create_reservation_list(self):
        incoming_test_values = [{
            'reservation_type': 'scrim',
            'base_id': Decimal('234'),
            'reservation_id': '2845ecf7-3ed6-4b0f-8887-90a8e6cb3f97',
            'start_time': Decimal('12456790'),
            'end_time': Decimal('12456789'),
            'event_day': Decimal('12441600'),
            'continent': 'amerish',
            'group_name': 'TEST'
        }]
        result = create_reservations_list(incoming_test_values)
        self.assertEqual(ReservationType.Scrim, result[0].reservation_type)
        self.assertEqual(ReservationContinent.Amerish, result[0].continent)
        self.assertEqual(12456790, result[0].start_time)

    def test_reservation_splitter(self):
        reservation = Reservation(
            facility_id=234,
            continent=ReservationContinent.Amerish,
            start_time=12456790,
            end_time=12456790 + (day_in_seconds * 2),
            group_name='Test',
            reservation_type=ReservationType.POG
        )
        start_day = get_event_day_from_timestamp(reservation.start_time)
        end_day = get_event_day_from_timestamp(reservation.end_time)
        result = reservation_splitter(reservation, start_day, end_day)
        self.assertEqual(3, len(result))
        # todo this provides 3 days. We need more tests for a mini-crossover day I guess 23:00 - 01:00?
        # todo a test for a full weekend. Which means Friday - Monday


if __name__ == '__main__':
    unittest.main()
