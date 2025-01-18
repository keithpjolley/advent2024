#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

import networkx as nx

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        if (len(args) > 1) and ("data/day18_test0.txt" == args[1]):
            self._w, self._h, self._steps = 7, 7, 12
        else:
            self._w, self._h, self._steps = 71, 71, 1024
        self._start = (0, 0)
        self._end = (self._w - 1, self._h - 1)
        self._raw_data = self._get_raw.raw_data.strip()
        self._graph = self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _draw(self: Self) -> None:  # pragma: no cover
        try:
            shortest_path = nx.shortest_path(
                self._graph, self._start, self._end
            )
        except nx.NetworkXNoPath:
            shortest_path = []
        colors = [
            "g" if n in shortest_path else "b" for n in self._graph.nodes()
        ]
        positions = {n: (n[0], -n[1]) for n in self._graph.nodes()}
        nx.draw(
            self._graph, pos=positions, node_color=colors, with_labels=False
        )

    def _parse_data(self: Self) -> list[list[int]]:
        graph = nx.Graph()
        graph.add_nodes_from(
            [(x, y) for x in range(self._h) for y in range(self._w)]
        )
        graph.add_edges_from(
            ((x, y), (x + 1, y))
            for x in range(self._w - 1)
            for y in range(self._h)
        )
        graph.add_edges_from(
            ((x, y), (x, y + 1))
            for x in range(self._w)
            for y in range(self._h - 1)
        )
        corrupts = [
            (int(x), int(y))
            for x, y in [
                pair.split(",")
                for pair in self._raw_data.split("\n")[: self._steps]
            ]
        ]
        graph.remove_nodes_from(corrupts)
        while (
            len(
                singletons := [
                    n
                    for n in graph.nodes
                    if graph.degree(n) < 2
                    and n not in [self._start, self._end]
                ]
            )
            > 0
        ):
            graph.remove_nodes_from(singletons)
        return graph

    def _part1(self: Self) -> int:
        return nx.shortest_path_length(self._graph, self._start, self._end)

    def _part2(self: Self) -> int:
        for corrupt in [
            (int(x), int(y))
            for x, y in [
                pair.split(",")
                for pair in self._raw_data.split("\n")[self._steps :]
            ]
        ]:
            if corrupt in self._graph.nodes:
                self._graph.remove_node(corrupt)
                try:
                    nx.shortest_path_length(
                        self._graph, self._start, self._end
                    )
                except nx.NetworkXNoPath:
                    return ",".join(str(c) for c in corrupt)
        return "No solution found."


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
