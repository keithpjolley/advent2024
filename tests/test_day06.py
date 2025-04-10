import unittest
from typing import Self

import numpy as np

import src.day06 as day


class TestDay06(unittest.TestCase):
    test_file = "data/day06_test0.txt"
    test_input = ["--input", test_file]
    good_data_result = np.array(
        [
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        ]
    )

    def test_parse_data(self: Self) -> None:
        test = day.day06(self.test_input)
        test_data = test._parse_data()
        self.assertEqual(test_data.tolist(), self.good_data_result.tolist())
        with self.assertRaises(ValueError) as cm:
            day.day06(["--input", "/dev/null"])
        the_exception = cm.exception
        err = "Invalid input data"
        self.assertEqual(str(the_exception), err)

    def test_parts(self: Self) -> None:
        tests = [(41, 6, self.test_input)]
        tests.append([38, 6, ["--input", "data/day06_test1.txt"]])
        tests.append([22, 5, ["--input", "data/day06_test2.txt"]])
        tests.append([26, 6, ["--input", "data/day06_test3.txt"]])
        # No use using up github action minutes for this.
        # tests.append((5331, 1812, []))
        for p1, p2, test in tests:
            test = day.day06(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(
                test.__str__(), f"Day 6: part 1: {p1}\nDay 6: part 2: {p2}"
            )
