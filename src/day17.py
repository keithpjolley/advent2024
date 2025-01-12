#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import operator
import os
import sys
import warnings
from itertools import batched

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Operands:

    def __init__(self: Self, a: int, b: int, c: int, program) -> None:
        self._output = []
        self._A = a
        self._B = b
        self._C = c
        self._program = program
        for reg, op in batched(self._program, n=2):
            self._exec(reg, op)

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        return "\n".join(
            (
                f"Register A: {self._A}",
                f"Register B: {self._B}",
                f"Register C: {self._C}",
                f"Program: {self._program}",
                f"Output: {','.join(map(str, self._output))}",
            )
        )

    def _exec(self: Self, instruction: int, operand: int) -> int:
        if operand == 4:
            combo = self._A
        elif operand == 5:
            combo = self._B
        elif operand == 6:
            combo = self._C
        else:
            if operand < 0 or operand > 6:
                warnings.warn(f"Invalid operand: '{operand}'", SyntaxWarning)
            combo = operand

        match instruction:
            case 0:
                self._adv(combo)
            case 1:
                self._bxl(combo)
            case 2:
                self._bst(combo)
            case 3:
                combo = self._jnz(combo)
            case 4:
                self._bxc()
            case 5:
                self._out(combo)
            case 6:
                self._bdv(combo)
            case 7:
                self._cdv(combo)

    def _adv(self, operand: int) -> int:
        self._A = int(self._A / 2**operand)

    def _bxl(self, operand: int) -> int:
        self._B = operator.xor(self._B, operand)

    def _bst(self, operand: int) -> int:
        self._B = operand % 8

    def _jnz(self, operand: int) -> int:
        if self._A == 0:
            return
        if operand != 3:
            self._exec(operand, operand)

    def _bxc(self) -> int:
        self._B = operator.xor(self._B, self._C)

    def _out(self, operand: int) -> int:
        self._output.append(operand % 8)

    def _bdv(self, operand: int) -> int:
        self._B = int(self._A / self._combo(operand))

    def _cdv(self, operand: int) -> int:
        self._C = int(self._A / self._combo(operand))


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
        self._operands = Operands(a, b, c, program)

    def _part1(self: Self) -> int:
        return 0

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
