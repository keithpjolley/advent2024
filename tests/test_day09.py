import unittest
from collections import deque
from typing import Self

import src.day09 as day


class TestDay(unittest.TestCase):
    test_file = "data/day09_test0.txt"
    test_input = ["--input", test_file]
    test_raw_data = "2333133121414131402"
    test_data = deque(
        [
            0,
            0,
            None,
            None,
            None,
            1,
            1,
            1,
            None,
            None,
            None,
            2,
            None,
            None,
            None,
            3,
            3,
            3,
            None,
            4,
            4,
            None,
            5,
            5,
            5,
            5,
            None,
            6,
            6,
            6,
            6,
            None,
            7,
            7,
            7,
            None,
            8,
            8,
            8,
            8,
            9,
            9,
        ]
    )

    def test_parse_data(self: Self) -> None:
        test = day.Day(self.test_input)
        self.assertEqual(test._raw_data, self.test_raw_data)
        self.assertEqual(test._data, self.test_data)

    def test_parts(self: Self) -> None:
        tests = [(1928, 2858, self.test_input)]
        # No use using up github action minutes for this.
        # tests.append((6340197768906, 6363913128533, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
