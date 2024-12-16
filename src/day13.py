#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    pass  # pragma: no cover

import os
import re
import sys
from collections import namedtuple

# from sympy.solvers.diophantine import diophantine
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
        """! Brute force and ignorance."""
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
        def _plot():  # pragma: no cover
            """! Left over from debugging."""

            def a(x):
                return slope_a * x

            def b(x):
                return slope_b * x

            def c(x):
                return b(x) + row.py - row.px * slope_b

            def d():
                return (row.py - row.px * slope_b) / (slope_a - slope_b)

            import matplotlib.pyplot as plt
            import numpy as np

            x = np.linspace(0, 50, 1000)
            fig, ax = plt.subplots()
            ax.plot(x, a(x), "-b", label="a(x)")
            ax.plot(x, b(x), "-r", label="b(x)")
            ax.plot(x, c(x), "-g", label="c(x)")
            ax.scatter(row.px, row.py, marker="o", color="black")
            ax.scatter(d(), a(d()), marker="+", color="black")
            ax.legend(loc="upper left")
            ax.grid()

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
                continue

            # tox showed this was never reached!
            if row is None:  # pragma: no cover
                if 9 * (row.mash_ay**2 + row.mash_ax**2) > (
                    row.mash_by**2 + row.mash_bx**2
                ):
                    # We want the cheaper route to be A.
                    # B is less tokens distance/mash, swap A and B
                    row = row._replace(
                        mash_ax=row.mash_bx,
                        mash_ay=row.mash_by,
                        mash_bx=row.mash_ax,
                        mash_by=row.mash_ay,
                        swapped=not row.swapped,
                    )
                # Can we get there directly by mashing A?
                if (
                    row.px % row.mash_ax == 0
                    and row.py % row.mash_ay == 0
                    and (a_mashes := row.px // row.mash_ax)
                    == row.py // row.mash_ay
                ):
                    # This is the cheapest route. Done.
                    total += (3 if not row.swapped else 1) * a_mashes
                    continue
                for a_mashes in range(1, row.px // row.mash_ax // 2 + 1):
                    # Can we get there by mashing A few times and then # mashing B?
                    if (
                        (row.px - a_mashes * row.mash_ax) % row.mash_bx == 0
                        and (row.py - a_mashes * row.mash_ay) % row.mash_by
                        == 0
                        and (
                            b_mashes := (row.px - a_mashes * row.mash_ax)
                            // row.mash_bx
                        )
                        == (row.py - a_mashes * row.mash_ay) // row.mash_by
                    ):
                        total += (3 if not row.swapped else 1) * a_mashes
                        continue
        return total


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))
