#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import re
import sys
from collections import namedtuple
from math import prod

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:

        self._seconds = 100
        self._test = len(args) > 1
        if self._test and "--input" in args and "test0" in args[1]:
            self._width = 11
            self._height = 7
        else:
            self._width = 101
            self._height = 103
        self._mid_width = self._width // 2
        self._mid_height = self._height // 2

        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._data = self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> list[list[int]]:
        nums = re.compile(r"-?\d+")
        row_tup = namedtuple("row", "px, py, vx, vy")
        return [
            row_tup._make(list(map(int, nums.findall(row))))
            for row in self._raw_data.splitlines()
        ]

    def _get_location(self, guard):
        x = (guard.px + (self._seconds * guard.vx)) % self._width
        y = (guard.py + (self._seconds * guard.vy)) % self._height
        return (x, y)

    def _get_quadrant(self, guard):
        x, y = self._get_location(guard)
        if x < self._mid_width and y < self._mid_height:
            return 0
        if x < self._mid_width and y > self._mid_height:
            return 1
        if x > self._mid_width and y < self._mid_height:
            return 2
        if x > self._mid_width and y > self._mid_height:
            return 3

    def _make_grid(self):
        grid = [[0 for _ in range(self._width)] for _ in range(self._height)]
        for guard in self._data:
            x, y = self._get_location(guard)
            grid[y][x] += 1
        grid = [["." if r == 0 else str(r) for r in row] for row in grid]
        return grid

    def _draw_map(self: Self):
        ret = f"Seconds: {self._seconds}"
        for j, row in enumerate(self._make_grid()):
            if j != self._mid_height:
                for i, r in enumerate(row):
                    if i == self._mid_width:
                        ret += " "
                    else:
                        ret += str(r) if r else "."
            ret += "\n"
        return ret

    def _part1(self: Self) -> int:
        quadrants = [0 for _ in range(4)]
        for guard in self._data:
            quadrant = self._get_quadrant(guard)
            if quadrant is not None:
                quadrants[quadrant] += 1
        return prod(quadrants)

    def _part2(self: Self) -> int:
        self._seconds = 7709
        if "11111111" in "\n".join(
            "".join(_ for _ in row) for row in self._make_grid()
        ):
            return self._seconds
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
