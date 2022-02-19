import unittest

from devispora.ovo_bases.app import lambda_handler


class AppTest(unittest.TestCase):
    def test_things(self):
        lambda_handler('', '')
