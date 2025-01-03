import unittest
from typing import Self

import src.day07 as day


class TestDay(unittest.TestCase):
    test_file = "data/day07_test0.txt"
    test_input = ["--input", test_file]
    test_raw_data = (
        "190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n"
        "7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n"
        "21037: 9 7 18 13\n292: 11 6 16 20"
    )
    test_data = [
        [190, [10, 19]],
        [3267, [81, 40, 27]],
        [83, [17, 5]],
        [156, [15, 6]],
        [7290, [6, 8, 6, 15]],
        [161011, [16, 10, 13]],
        [192, [17, 8, 14]],
        [21037, [9, 7, 18, 13]],
        [292, [11, 6, 16, 20]],
    ]

    def test_parse_data(self: Self) -> None:
        test = day.Day(self.test_input)
        self.assertEqual(test._raw_data, self.test_raw_data)
        self.assertEqual(test._data, self.test_data)

    def test_parts(self: Self) -> None:
        p1, p2 = 3749, 11387
        test = day.Day(self.test_input)
        self.assertEqual(test.p2, p2)
        self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
        # p1, p2 = 5331, 1812
        # test = day.Day()
        # self.assertEqual(test.p2, p2)
        # self.assertEqual(
        #     test.__str__(), f"part 1: {p1}\npart 2: {p2}"
        # )
