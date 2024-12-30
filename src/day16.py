#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys

import networkx as nx

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

    def _parse_data(self: Self) -> list[list[int]]:
        graph = nx.Graph()
        for j, row in enumerate(self._raw_data.split("\n")):
            for i, col in enumerate(row.split()):
                if col != "#":
                    graph.add_node(f"{i:02d}.{j:02d}}", value=int(col))
            self._data.append(list(map(int, row.split())))
        return self._raw_data

    def _part1(self: Self) -> int:
        return 0

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
