import unittest
from typing import Self

import src.day18 as day


class TestDay(unittest.TestCase):
    test_input = ["--input", "data/day18_test0.txt"]

    def test_parts(self: Self) -> None:
        tests = [
            (22, "6,1", self.test_input),
            (140, "No solution found.", ["--input", "data/day18_test1.txt"]),
        ]
        # No use using up github action minutes for this.
        # tests.append((0, 0, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
