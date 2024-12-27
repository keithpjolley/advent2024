import unittest
from typing import Self

import src.day14 as day


class TestDay(unittest.TestCase):
    _test_input = ["--input", "data/day14_test0.txt"]
    _test_data = [
        {"px": 0, "py": 4, "vx": 3, "vy": -3},
        {"px": 6, "py": 3, "vx": -1, "vy": -3},
        {"px": 10, "py": 3, "vx": -1, "vy": 2},
        {"px": 2, "py": 0, "vx": 2, "vy": -1},
        {"px": 0, "py": 0, "vx": 1, "vy": 3},
        {"px": 3, "py": 0, "vx": -2, "vy": -2},
        {"px": 7, "py": 6, "vx": -1, "vy": -3},
        {"px": 3, "py": 0, "vx": -1, "vy": -2},
        {"px": 9, "py": 3, "vx": 2, "vy": 3},
        {"px": 7, "py": 3, "vx": -1, "vy": 2},
        {"px": 2, "py": 4, "vx": 2, "vy": -3},
        {"px": 9, "py": 5, "vx": -3, "vy": -3},
    ]

    def test_parse_args(self: Self) -> None:
        test = day.Day(self._test_input)
        self.assertEqual(
            [row._asdict() for row in test._data], self._test_data
        )

    def test_parts(self: Self) -> None:
        tests = [(12, 0, self._test_input)]
        tests.append((230435667, 7709, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
