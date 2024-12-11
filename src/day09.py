#!/usr/bin/env python3

import itertools as it
import os
import sys
from collections import deque
from typing import Never, Self

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    def _parse_data(self: Self) -> deque:
        """! Parse the input data into a numpy array.
        @param data: The input map, a string.
        @return: A tuple containing the map and the starting point.
        """
        return deque(
            i // 2 if i % 2 == 0 else None
            for i, faf in enumerate(int(x) for x in self._raw_data)
            for _ in range(faf)
        )

    def _part1(self: Self) -> int:
        data = self._data.copy()
        try:
            while i := data.index(None):
                data[i] = data.pop()
        except (IndexError, ValueError):
            return sum(i * f for i, f in enumerate(data) if f is not None)

    def _get_holes(self: Self, data: list[None] | list[int]) -> dict[int, int]:
        # return dict of {hole_start: hole_length, ...}
        holes = [[_, len(list(g))] for _, g in it.groupby(data)]
        hole_index = [0] + list(it.accumulate([h[1] for h in holes][:-1]))
        return {b: a[1] for a, b in zip(holes, hole_index) if a[0] is None}

    def _part2(self: Self) -> int:
        data = list(self._data)
        for _, g in it.groupby(reversed(self._data)):
            g = list(g)
            if g[0] is None:
                continue
            holes = self._get_holes(data)
            for hole_start, hole_length in holes.items():
                if hole_length >= len(g):
                    g_start = data.index(g[0])
                    if g_start < hole_start:
                        continue
                    data[hole_start : hole_start + len(g)] = g
                    data[g_start : g_start + len(g)] = [None] * len(g)
                    break
        return sum(i * f for i, f in enumerate(data) if f is not None)


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
