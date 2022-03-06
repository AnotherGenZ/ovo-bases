import unittest

from devispora.ovo_bases.models.reservations import Reservation, ReservationContinent, ReservationType
from devispora.ovo_bases.processor.availability_processor import check_if_available


class AvailabilityProcessorTest(unittest.TestCase):

    def test_check_if_available_denied(self):
        # Arrange
        incoming_reservations = [
            Reservation(
                continent=ReservationContinent.Hossin,
                facility_id=302030,
                reservation_type=ReservationType.Scrim,
                group_name='New Group',
                start_time=1628445600,
                end_time=1628452800
            )
        ]

        stored_reservations = [
            Reservation(
                continent=ReservationContinent.Hossin,
                facility_id=302030,
                reservation_type=ReservationType.Scrim,
                group_name='Old group',
                start_time=1628449200,
                end_time=1628456400
            )]

        # Act
        result = check_if_available(incoming_reservations, stored_reservations)
        # Assert
        self.assertEqual(1, len(result.denied_reservations))
        self.assertEqual(0, len(result.possible_reservations))

    def test_check_if_available_approved(self):
        # Arrange
        incoming_reservations = [
            Reservation(
                continent=ReservationContinent.Hossin,
                facility_id=302030,
                reservation_type=ReservationType.Scrim,
                group_name='New Group',
                start_time=1628445600,
                end_time=1628452800
            )
        ]
        stored_reservations = [
            Reservation(
                continent=ReservationContinent.Hossin,
                facility_id=302030,
                reservation_type=ReservationType.Scrim,
                group_name='Old group',
                start_time=1628452800,
                end_time=1628456400
            )]
        # Act
        result = check_if_available(incoming_reservations, stored_reservations)
        # Assert
        self.assertEqual(0, len(result.denied_reservations))
        self.assertEqual(1, len(result.possible_reservations))

    def test_check_if_available_denied_kessels(self):
        # Arrange
        incoming_reservations = [
            Reservation(
                continent=ReservationContinent.Hossin,
                facility_id=266000,
                reservation_type=ReservationType.Scrim,
                group_name='New Group',
                start_time=1628445600,
                end_time=1628452800
            )
        ]
        stored_reservations = [
            Reservation(
                continent=ReservationContinent.Hossin,
                facility_id=307010,
                reservation_type=ReservationType.Scrim,
                group_name='Old group',
                start_time=1628449200,
                end_time=1628456400
            )]

        # Act
        result = check_if_available(incoming_reservations, stored_reservations)
        # Assert
        self.assertEqual(1, len(result.denied_reservations))
        self.assertEqual(0, len(result.possible_reservations))

# todo add test that takes existing reservations during the same time into account to compare to.
#  error has been fixed already, but it gotta stay that way.
# todo add large event test and perhaps some burst small ones
