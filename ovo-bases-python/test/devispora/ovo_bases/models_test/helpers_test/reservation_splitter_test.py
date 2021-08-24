import unittest

from devispora.ovo_bases.models.helpers.reservation_splitter import reservation_splitter
from devispora.ovo_bases.models.reservations import Reservation, ReservationContinent, ReservationType
from devispora.ovo_bases.tools.time_service import get_event_day_from_timestamp, one_hour_in_seconds, day_in_seconds


class ReservationSplitterTest(unittest.TestCase):

    def test_reservation_splitter_three_reservations(self):
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

    def test_reservation_splitter_two_reservations(self):
        reservation = Reservation(
            facility_id=234,
            continent=ReservationContinent.Amerish,
            start_time=2847000,
            end_time=2847000 + (one_hour_in_seconds * 4),
            group_name='Test',
            reservation_type=ReservationType.POG
        )
        start_day = get_event_day_from_timestamp(reservation.start_time)
        end_day = get_event_day_from_timestamp(reservation.end_time)
        result = reservation_splitter(reservation, start_day, end_day)
        self.assertEqual(2, len(result))

    def test_reservation_splitter_four_reservations(self):
        reservation = Reservation(
            facility_id=234,
            continent=ReservationContinent.Amerish,
            start_time=3192600,
            end_time=3376200,
            group_name='Test',
            reservation_type=ReservationType.POG
        )
        start_day = get_event_day_from_timestamp(reservation.start_time)
        end_day = get_event_day_from_timestamp(reservation.end_time)
        result = reservation_splitter(reservation, start_day, end_day)
        self.assertEqual(4, len(result))


if __name__ == '__main__':
    unittest.main()
