#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import re
import sys
from collections import namedtuple
from fractions import Fraction
from itertools import batched

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
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
        nums = re.compile(r"\d+")
        row_tup = namedtuple(
            "row",
            "mash_ax, mash_ay, mash_bx, mash_by, px, py, swapped",
        )
        return [
            row_tup._make(
                list(map(int, nums.findall("".join(rows[:3])))) + [False]
            )
            for rows in batched(self._raw_data.splitlines(), 4)
        ]

    def _part1(self: Self) -> int:
        """! Brute force and ignorance ftw."""
        total = 0
        for i, row in enumerate(self._data):
            # Won't push any more than this many times for Button A.
            max_mash_a = min(row.px // row.mash_ax, row.py // row.mash_ay)
            # Won't push any more than this many times for Button B.
            max_mash_b = min(row.px // row.mash_bx, row.py // row.mash_by)
            # A starts at the origin and goes to prize.
            a_locations = [
                (i * row.mash_ax, i * row.mash_ay)
                for i in range(max_mash_a + 1)
            ]
            # B starts at the prize and goes to the origin.
            b_locations = [
                (row.px - i * row.mash_bx, row.py - i * row.mash_by)
                for i in range(max_mash_b + 1)
            ]
            try:
                total += min(
                    3 * a_mash + b_locations.index(loc)
                    for a_mash, loc in enumerate(a_locations)
                    if loc in b_locations
                )
            except ValueError:
                total += 0
        return total

    def _part2(self: Self) -> int:
        total = 0
        adder = 10000000000000
        for row in self._data:
            row = row._replace(px=row.px + adder, py=row.py + adder)
            slope_a = Fraction(row.mash_ay, row.mash_ax)
            slope_b = Fraction(row.mash_by, row.mash_bx)
            slope_p = Fraction(row.py, row.px)
            # Too steep?
            if slope_a > slope_p and slope_b > slope_p:
                # Can't get there from here. Done.
                continue
            # Too shallow?
            if slope_a < slope_p and slope_b < slope_p:
                continue
            # Apparently there are no cases where the slopes.
            if slope_a != slope_b:
                # Find where the triangles intersect. There will be one
                # such point.
                #
                #                           + (px, py)
                #                          /|
                #                        b/ |
                #                        /  |
                #     intersection --> +/..:|
                #                  ...:/    |
                #           a ....:   /     |
                #          ..:       /      |
                #     0,0 +---------+-------+
                #
                #     a(mash_a) = mash_ay / mash_ax * mash_a
                #     b(mash_b) = mash_bx / mash_by * mash_b
                #
                x_intercept = (row.py - row.px * slope_b) / (slope_a - slope_b)
                y_intercept = slope_a * x_intercept
                # Can we get to this point by mashing A and...
                # can we get from this point to the prize by mashing B...
                # and we can't have imaginary mashes.  The number of
                # mashes on A to get to the point have to be the same
                # as well as from the point to the prize.
                # Also, how cool is it to use the walrus operator?
                if (
                    x_intercept % row.mash_ax == 0
                    and y_intercept % row.mash_ay == 0
                    and (row.px - x_intercept) % row.mash_bx == 0
                    and (row.py - y_intercept) % row.mash_by == 0
                    and (a_mashes := x_intercept // row.mash_ax)
                    == y_intercept // row.mash_ay
                    and (b_mashes := (row.px - x_intercept) // row.mash_bx)
                    == (row.py - y_intercept) // row.mash_by
                ):
                    total += 3 * a_mashes + b_mashes
        return total


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))
