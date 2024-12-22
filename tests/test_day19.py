import unittest
from typing import Self

import src.day19 as day


class TestDay(unittest.TestCase):
    test_input = ["--input", "data/day19_test0.txt"]
    test_patterns = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
    test_designs = [
        "brwrr",
        "bggr",
        "gbbr",
        "rrbgbr",
        "ubwu",
        "bwurrg",
        "brgr",
        "bbrgwb",
    ]

    def test_parse_args(self: Self) -> None:
        test = day.Day(self.test_input)
        self.assertEqual(test._patterns, self.test_patterns)
        self.assertEqual(test._designs, self.test_designs)

    def test_parts(self: Self) -> None:
        tests = [(6, 0, self.test_input)]
        tests.append((311, 0, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
