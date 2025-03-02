import unittest
from typing import Self

import src.day24 as day


class TestDay(unittest.TestCase):

    def test_parts(self: Self) -> None:
        hard_coded_answer_for_part_two = "djg,dsd,hjm,mcq,sbg,z12,z19,z37"
        tests = [
            (
                4,
                hard_coded_answer_for_part_two,
                ["--input", "data/day24_test0.txt"],
            )
        ]
        tests.append(
            (
                2024,
                hard_coded_answer_for_part_two,
                ["--input", "data/day24_test1.txt"],
            ),
        )
        tests.append(
            (64755511006320, hard_coded_answer_for_part_two, []),
        )
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
