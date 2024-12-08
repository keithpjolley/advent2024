import unittest

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

    def test_parse_data(self):
        test = day.day06(self.test_input)
        test_data = test._parse_data()
        self.assertEqual(test_data.tolist(), self.good_data_result.tolist())
        with self.assertRaises(ValueError) as cm:
            day.day06(["--input", "/dev/null"])
        the_exception = cm.exception
        err = "Invalid input data"
        self.assertEqual(str(the_exception), err)

    def test_parts(self):
        p1, p2 = 41, 6
        test = day.day06(self.test_input)
        self.assertEqual(test.p2, p2)
        self.assertEqual(
            test.__str__(), f"Day 6: part 1: {p1}\nDay 6: part 2: {p2}"
        )
        # p1, p2 = 5331, 1812
        # test = day.day06()
        # self.assertEqual(test.p2, p2)
        # self.assertEqual(
        #     test.__str__(), f"Day 6: part 1: {p1}\nDay 6: part 2: {p2}"
        # )
