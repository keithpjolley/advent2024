import unittest
from typing import Self

import src.day23 as day


class TestDay(unittest.TestCase):
    test_input = ["--input", "data/day23_test0.txt"]
    test_data = []

    def test_parts(self: Self) -> None:
        tests = [(7, "co,de,ka,ta", self.test_input)]
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
