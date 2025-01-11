#!/usr/bin/env python3

# I struggled to figure out how to do a pure networkx solution for this
# problem. My first iteration was to create a graph using networkx but
# I couldn't figure out how to make it so the shortest path algo would
# know to use the different weights for turning vs going straight. So I
# abandoned that approach and created the graph using networkx and then
# fed that graph into a custom dijkstra algo. Then expanded that to get
# all shortest paths.

# Then I read this solution:
# https://github.com/fuglede/adventofcode/blob/master/2024/day16/solutions.py
# and plagerized the heck out of it.

# I'm still figuring out exactly how it works, how it has the "memory"
# to use the different weight of turning or going straight. I have my
# intuition that says it sort of makes four copies, or levels, of the
# graph but I have to create some better visualizations to really grok
# this. I think it's incredibly clever and I'm eager to learn more about
# it. I wish I'd figured it out for myself (even though I am glad I was
# able to brute force it on my own).

from typing import TYPE_CHECKING, Never, Self

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
        self._raw_data = self._get_raw.raw_data.strip().split("\n")
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
        directions = (1, -1, 1j, -1j)
        self._graph = nx.DiGraph()
        for i, row in enumerate(self._raw_data):
            for j, col in enumerate(row):
                if col == "#":
                    continue
                point = i + 1j * j
                if col == "S":
                    self._start = (point, 1j)
                if col == "E":
                    end = point
                for direction in directions:
                    self._graph.add_node((point, direction))

        for point, direction in self._graph.nodes:
            if (point + direction, direction) in self._graph.nodes:
                # weight 1 to go straight
                self._graph.add_edge(
                    (point, direction),
                    (point + direction, direction),
                    weight=1,
                )
            for turn in -1j, 1j:
                # weight 1000 to turn
                self._graph.add_edge(
                    (point, direction), (point, direction * turn), weight=1000
                )

        for direction in directions:
            self._graph.add_edge((end, direction), "E", weight=0)

    def _part1(self: Self) -> int:
        return nx.shortest_path_length(
            self._graph, self._start, "E", weight="weight"
        )

    def _part2(self: Self) -> int:
        asps = nx.all_shortest_paths(
            self._graph, self._start, "E", weight="weight"
        )
        return len({node for asp in asps for node, _ in asp[:-1]})


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
