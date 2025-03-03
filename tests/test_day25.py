import unittest
from typing import Self

import src.day25 as day


class TestDay(unittest.TestCase):

    def test_parts(self: Self) -> None:
        tests = [(3, 0, ["--input", "data/day25_test0.txt"])]
        tests.append((2854, 0, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
