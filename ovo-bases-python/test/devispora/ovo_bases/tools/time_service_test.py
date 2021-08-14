import unittest
from decimal import Decimal

from devispora.ovo_bases.tools.time_service import get_event_day_from_timestamp


class TimeServiceTest(unittest.TestCase):
    def test_get_event_day_from_timestamp(self):
        july_29_and_a_second = 1627516801
        july_29 = 1627516800
        result = get_event_day_from_timestamp(july_29_and_a_second)
        self.assertEqual(july_29, result)


if __name__ == '__main__':
    unittest.main()
