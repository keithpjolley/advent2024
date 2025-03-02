import unittest
from typing import Self

import src.day22 as day


class TestDay(unittest.TestCase):
    def test_parts(self: Self) -> None:
        # for test, a1, a2 in [(0, 37327623, 23), (1, 37990510, 23)]:
        for test, a1, a2 in [(0, -1, 24), (1, -1, 25)]:
            test = day.Day(["--input", f"data/day22_test{test}.txt"])
            self.assertEqual(test.p1, a1)
            self.assertEqual(test.p2, a2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {a1}\npart 2: {a2}")
