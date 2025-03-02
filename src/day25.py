#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys
from itertools import product

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._locks = []
        self._keys = []
        self._raw_data = self._get_raw.raw_data.strip()
        self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> None:

        def rotate(data: list[list[str]]) -> (bool, list[list[str]]):
            lock = data[0].count("#") == len(data[0]) and data[-1].count(
                "."
            ) == len(data[-1])
            return (
                lock,
                len(data[0]),
                [row.count("#") - 1 for row in zip(*data)],
            )

        for thing in self._raw_data.split("\n\n"):
            lock, size, device = rotate(
                [[y for y in x] for x in thing.split()]
            )
            if lock:
                self._locks.append((device, size))
            else:
                self._keys.append((device, size))

    def _part1(self: Self) -> int:
        return sum(
            all(k + l <= max_kl for k, l in zip(key, lock))
            for (key, max_kl), (lock, max_ll) in product(
                self._keys, self._locks
            )
        )

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
