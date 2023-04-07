import unittest
from functions.my_functions import *

class FunctionsTestCase(unittest.TestCase):
    """Tests for functions in the my_functions.py file"""

    def test_validate_valid_cc(self):
        """Tests valid values for a credit card"""
        tests = ["1234567890123", "1234 5678 9012 3456", "491 62360 69264 633", "471 67892 55235 322", "4916726420980"]

        for test in tests:
            self.assertTrue(validate_cc(test))

    def test_validate_invalid_cc(self):
        """Tests invalid values for a credit card"""
        tests = ["  1234567890123", "00000000000000000000", "1", "471 67892 55235 322 331 612", "CC: 49166420980111"]

        for test in tests:
            self.assertFalse(validate_cc(test))

    def test_validate_valid_coords(self):
        """Tests valid values for coordinates"""
        tests = ["34.35302, 8.5588", "-31.41587, -179.67423", "-31.11404, 111.42736", "99.9999, -99.9999"]

        for test in tests:
            self.assertTrue(validate_coords(test))

    def test_validate_invalid_coords(self):
        """Tests invalid values for coordinates"""
        tests = ["-1211.1111, 155.51111", "99.9999,-99.9999", " 1.111, -1.111 ", "1.123,  -1.123", "Coords: 31.4411, 41.1144"]

        for test in tests:
            self.assertFalse(validate_coords(test))

    def test_validate_valid_money(self):
        """Tests valid values for money"""
        tests = ["$1,000", "$5,909", "$9,999"]

        for test in tests:
            self.assertTrue(validate_money(test))

    def test_validate_invalid_money(self):
        """Tests invalid values for money"""
        tests = ["5,111", " $1,211", "$123", "$0", "Dollars: $1,999"]

        for test in tests:
            self.assertFalse(validate_money(test))