import unittest
from typing import Self

import src.day08 as day


class TestDay(unittest.TestCase):
    test_file = "data/day08_test0.txt"
    test_input = ["--input", test_file]
    test_raw_data = """............
        ........0...
        .....0......
        .......0....
        ....0.......
        ......A.....
        ............
        ............
        ........A...
        .........A..
        ............
        ............""".replace(
        " ", ""
    )
    test_data = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "0", ".", ".", "."],
        [".", ".", ".", ".", ".", "0", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "0", ".", ".", ".", "."],
        [".", ".", ".", ".", "0", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "A", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "A", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", ".", "A", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    ]

    def test_parse_data(self: Self) -> None:
        test = day.Day(self.test_input)
        self.assertEqual(test._raw_data, self.test_raw_data)
        self.maxDiff = None
        self.assertEqual(test._data, self.test_data)

    def test_parts(self: Self) -> None:
        tests = [(14, 34, self.test_input)]
        # No use using up github action minutes for this.
        # tests.append((311, 1115, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
