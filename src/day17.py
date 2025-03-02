#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Operands:

    def __init__(
        self: Self, a: int, b: int, c: int, program: list[int]
    ) -> None:
        self._A = a
        self._B = b
        self._C = c
        self.program = program
        self.output = []
        self._exec()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        return "\n".join(
            (
                f"Register A: {self._A}",
                f"Register B: {self._B}",
                f"Register C: {self._C}",
                f"Program: {self.program}",
                f"Output: {','.join(map(str, self.output))}",
            )
        )

    def _exec(self: Self) -> None:

        index = 0

        while True:

            try:
                instruction, operand = (
                    self.program[index],
                    self.program[index + 1],
                )
            except IndexError:
                return

            try:
                combo = [0, 1, 2, 3, self._A, self._B, self._C][operand]
            except IndexError:
                combo = operand

            match instruction:
                case 0:
                    self._A >>= combo
                case 1:
                    self._B ^= combo
                case 2:
                    self._B = combo % 8
                case 3:
                    if self._A:
                        index = operand - 2
                case 4:
                    self._B ^= self._C
                case 5:
                    self.output.append(combo % 8)
                case 6:
                    self._B = self._A >> combo
                case 7:
                    self._C = self._A >> combo

            index += 2


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.split("\n")
        self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> list[list[int]]:
        """! Sample input:
        Register A: 729
        Register B: 0
        Register C: 0

        Program: 0,1,5,4,3,0
        """
        for line in self._raw_data:
            if ":" not in line:
                continue
            input_type, value = line.split(":")
            if input_type == "Register A":
                a = int(value)
            elif input_type == "Register B":
                b = int(value)
            elif input_type == "Register C":
                c = int(value)
            elif input_type == "Program":
                program = [int(i) for i in value.split(",")]
        self.operands = Operands(a, b, c, program)

    def _part1(self: Self) -> str:
        return ",".join(str(i) for i in self.operands.output)

    def _part2(self: Self) -> int:
        # Solve from the tail end of the program to the front, 3 bits at a time.
        program = self.operands.program
        reg_a = 0
        for i in reversed(range(len(program))):
            reg_a <<= 3
            while Operands(reg_a, 0, 0, program).output != program[i:]:
                reg_a += 1
        return reg_a


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
