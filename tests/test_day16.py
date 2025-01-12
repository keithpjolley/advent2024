import unittest
from typing import Self

import src.day16 as day


class TestDay(unittest.TestCase):
    test_input = ["--input", "data/day16_test0.txt"]
    test_data = []

    # def test_parse_args(self: Self) -> None:
    #     test = day.Day(self.test_input)
    #     self.assertEqual(test._data, self.test_data)

    def test_parts(self: Self) -> None:
        tests = [(7036, 45, self.test_input)]
        # No use using up github action minutes for this.
        # tests.append((0, 0, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
