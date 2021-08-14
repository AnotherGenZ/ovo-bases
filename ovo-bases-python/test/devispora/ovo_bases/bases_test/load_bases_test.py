import unittest
import os
import json

from devispora.ovo_bases.bases.load_bases import determine_source


class LoadBasesTest(unittest.TestCase):

    def test_determine_source(self):
        os.environ['MAP_REGION_LOCATION'] = '../../../resources/map_region.json'
        result = determine_source()
        map_file = None
        try:
            map_file = open(result)
            loaded_map = json.load(map_file)
            assert 'map_region_list' in loaded_map
        except IOError:
            print("File not accessible")
            raise
        finally:
            map_file.close()


if __name__ == '__main__':
    unittest.main()
