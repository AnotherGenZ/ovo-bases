import unittest
from decimal import Decimal

from devispora.ovo_bases.models.reservation_helper import create_reservations_list
from devispora.ovo_bases.models.reservations import ReservationType, ReservationContinent


class ReservationHelperTest(unittest.TestCase):
    def test_create_reservation_list(self):
        incoming_test_values = [{
            'event_type': 'scrim',
            'base_id': Decimal('234'),
            'reservation_id': '2845ecf7-3ed6-4b0f-8887-90a8e6cb3f97',
            'start_time': Decimal('12456790'),
            'end_time': Decimal('12456789'),
            'event_day': Decimal('12441600'),
            'continent': 'amerish',
            'group_name': 'TEST'
        }]
        result = create_reservations_list(incoming_test_values)
        self.assertEqual(ReservationType.Scrim, result[0].event_type)
        self.assertEqual(ReservationContinent.Amerish, result[0].continent)
        self.assertEqual(12456790, result[0].start_time)
