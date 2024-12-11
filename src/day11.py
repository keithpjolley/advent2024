#!/usr/bin/env python3

import os
import sys
from typing import Self

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math import floor, log

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[str]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._data = self._parse_data()
        self._my_rules = {}
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> list[list[int]]:
        return [int(c) for c in self._raw_data.split()]

    def _do_rule(self: Self, stone: int, count: int) -> int:
        """! Recursion with lookup table."""
        if count == 0:
            return 1

        if (stone, count) in self._my_rules:
            return self._my_rules[(stone, count)]

        if stone == 0:
            size = self._do_rule(1, count - 1)

        elif (lss := floor(log(stone, 10)) + 1) % 2 == 0:
            lss //= 2
            size = self._do_rule(
                stone // 10**lss, count - 1
            ) + self._do_rule(stone % 10**lss, count - 1)
        else:
            size = self._do_rule(stone * 2024, count - 1)

        if (stone, count) not in self._my_rules:
            self._my_rules[(stone, count)] = size
        return size

    def _part1(self: Self) -> int:
        return sum(self._do_rule(stone, 25) for stone in self._data.copy())

    def _part2(self: Self) -> int:
        return sum(self._do_rule(stone, 75) for stone in self._data.copy())


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
