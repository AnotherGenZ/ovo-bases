import unittest

from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.reservations import Reservation, ReservationContinent, ReservationType
from devispora.ovo_bases.tools.time_service import day_in_seconds
from devispora.ovo_bases.validation.reservation_validation import start_not_in_long_past, create_current_epoch, \
    starts_before_end, start_not_far_from_end


class ReservationValidationTest(unittest.TestCase):

    def test_start_not_in_long_past_negative_incorrect(self):
        now = create_current_epoch()
        bad_reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=now - 3700,
            end_time=12456789
        )
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.MoreThanOneHourAgo,
            start_not_in_long_past, reservation=bad_reservation
        )

    def test_start_not_in_long_past_negative_correct(self):
        now = create_current_epoch()
        ok_reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=now - 1000,
            end_time=12456789
        )
        self.assertTrue(start_not_in_long_past(ok_reservation))

    def test_start_not_in_long_past_positive_correct(self):
        now = create_current_epoch()
        ok_reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=now + 9000,
            end_time=12456789
        )
        self.assertTrue(start_not_in_long_past(ok_reservation))

    def test_starts_before_end_incorrect(self):
        bad_reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=12999999,
            end_time=12456789
        )
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.StartAfterEnd,
            starts_before_end, reservation=bad_reservation
        )

    def test_starts_before_end_correct(self):
        ok_reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=12456788,
            end_time=12456789
        )
        self.assertTrue(starts_before_end(reservation=ok_reservation))

    def test_start_not_far_from_end_incorrect(self):
        bad_reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=12456788,
            end_time=12456789 + (day_in_seconds * 3) + 1
        )
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.MoreThanThreeDAys,
            start_not_far_from_end, reservation=bad_reservation
        )

    def test_start_not_far_from_end_correct(self):
        reservation = Reservation(
            base_id=230,
            continent=ReservationContinent.Hossin,
            event_type=ReservationType.Scrim,
            group_name='TEST',
            start_time=12456788,
            end_time=12456788 + (day_in_seconds * 3)
        )
        result = start_not_far_from_end(reservation)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
