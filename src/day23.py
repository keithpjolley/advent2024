#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip().split("\n")
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
        for line in self._raw_data:
            graph.add_edge(*line.split("-"), weight=1)
        return graph

    def _part1(self: Self) -> int:
        return len(
            [
                c
                for c in nx.enumerate_all_cliques(self._data)
                if len(c) == 3
                if any(n.startswith("t") for n in c)
            ]
        )

    def _part2(self: Self) -> int:
        return ",".join(
            sorted(
                sorted(
                    [c for c in nx.enumerate_all_cliques(self._data)],
                    key=lambda x: -len(x),
                )[0]
            )
        )


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
