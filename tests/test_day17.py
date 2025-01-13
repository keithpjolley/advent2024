import unittest
from typing import Self

import src.day17 as day


class TestDay(unittest.TestCase):

    test_input = ["--input", "data/day17_test1.txt"]

    def test_operands(self: Self) -> None:
        test_op = day.Operands(0, 0, 9, [2, 6])
        self.assertEqual(test_op._A, 0)
        self.assertEqual(test_op._B, 1)
        self.assertEqual(test_op._C, 9)
        self.assertEqual(test_op.program, [2, 6])
        self.assertEqual(test_op.output, [])

        test_op = day.Operands(10, 0, 0, [5, 0, 5, 1, 5, 4])
        self.assertEqual(test_op.output, [0, 1, 2])

        self.assertEqual(day.Operands(10, 0, 0, [0, 2])._A, 2)
        self.assertEqual(day.Operands(10, 1, 0, [0, 5])._A, 5)

        test_op = day.Operands(2024, 0, 0, [0, 1, 5, 4, 3, 0])
        self.assertEqual(test_op._A, 0)
        self.assertEqual(test_op.output, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0])

        self.assertEqual(day.Operands(0, 29, 0, [1, 7])._B, 26)

        self.assertEqual(day.Operands(0, 2024, 43690, [4, 0])._B, 44354)

        self.assertEqual(day.Operands(255, 255, 255, [6, 1, 7, 1]).output, [])
        out = (
            "Register A: 255\n"
            "Register B: 127\n"
            "Register C: 127\n"
            "Program: [6, 1, 7, 1]\n"
            "Output: "
        )
        self.assertEqual(str(day.Operands(255, 255, 255, [6, 1, 7, 1])), out)

    def test_parts(self: Self) -> None:
        tests = [("5,7,3,0", 117440, self.test_input)]
        # No use using up github action minutes for this.
        # tests.append((0, 0, []))
        for p1, p2, test in tests:
            test = day.Day(test)
            self.assertEqual(test.p1, p1)
            self.assertEqual(test.p2, p2)
            # Makes sure the __str__ function is covered.
            self.assertEqual(test.__str__(), f"part 1: {p1}\npart 2: {p2}")
