import unittest
import os

from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.bases.search_base import retrieve_base_by_id


class ParseBasesTest(unittest.TestCase):
    def test_load_bases(self):
        # Arrange
        hvar_base_id = 7500
        extra_base_id = 400022
        os.environ['MAP_REGION_LOCATION'] = '../../../resources/map_region.json'
        parser = BaseParser()
        # Act
        parser.create_base_list()
        # Assert
        # Normal bases
        result = retrieve_base_by_id(parser.stored_facilities, hvar_base_id)
        self.assertEqual(hvar_base_id, result.facility_id)
        self.assertEqual('Hvar Tech Plant', result.facility_name_long)
        # # Extra loaded bases
        result_extra = retrieve_base_by_id(parser.stored_facilities, extra_base_id)
        self.assertEqual('Koltyr Amp Station Outpost', result_extra.facility_name)


if __name__ == '__main__':
    unittest.main()
