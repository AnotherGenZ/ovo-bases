import unittest

from devispora.ovo_bases.models.facility_helper import find_reservation_continent_by_zone_id
from devispora.ovo_bases.models.reservations import ReservationContinent


class FacilityHelperTest(unittest.TestCase):
    def test_find_reservation_continent_by_zone_id_indar_found(self):
        indar = 2
        result = find_reservation_continent_by_zone_id(indar)
        self.assertEqual(ReservationContinent.Indar, result)
