import os
import unittest

from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.helpers.facility_helper import find_reservation_continent_by_zone_id, find_facilities
from devispora.ovo_bases.models.reservations import ReservationContinent


class FacilityHelperTest(unittest.TestCase):
    def test_find_reservation_continent_by_zone_id_indar_found(self):
        indar = 2
        result = find_reservation_continent_by_zone_id(indar)
        self.assertEqual(ReservationContinent.Indar, result)

    def test_find_facilities_empty_list(self):
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.FacilityNotProvided,
            find_facilities, base_parser=None, requested_facilities=[]
        )

    def test_find_facilities_bad_value(self):
        self.assertRaisesRegex(
            RequestException, RequestExceptionMessage.FacilityCannotBeFound,
            find_facilities, base_parser=None, requested_facilities=['name']
        )

    def test_find_facilities_succeed(self):
        hvar_base_id = 7500
        extra_base_id = 400022
        os.environ['MAP_REGION_LOCATION'] = '../../../../resources/map_region.json'
        parser = BaseParser()
        # Act
        parser.create_base_list()
        result = find_facilities(base_parser=parser, requested_facilities=[hvar_base_id, extra_base_id])
        self.assertEqual(hvar_base_id, result[0].facility_id)
        self.assertEqual(extra_base_id, result[1].facility_id)


if __name__ == '__main__':
    unittest.main()
