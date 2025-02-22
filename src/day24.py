#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

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

    def _draw_graph(self: Self) -> None:
        pos = nx.kamada_kawai_layout(self._data)
        nx.draw(self._data, pos, with_labels=True)

    def _parse_data(self: Self) -> list[list[int]]:
        gates = False
        graph = nx.DiGraph()
        for line in self._raw_data.splitlines():
            if gates:
                (n0, op, n1, _, n2) = line.split()
                opnode = f"{n0}-{op}-{n1}"
                graph.add_node(opnode, function=op, value=None)
                graph.add_edges_from(
                    [(n0, opnode), (n1, opnode), (opnode, n2)]
                )
            elif line == "":
                gates = True
            else:
                (n0, value) = line.split(": ")
                graph.add_node(n0, value=value)
        return graph

    def _part1(self: Self) -> int:
        # for nodes in list(nx.topological_generations(self._graph))[1:]:
        #     for node in nodes:
        #         if self._graph.nodes[node]["value"] is None:
        #             n0 = list(self._graph.predecessors(node))[0]
        #             n1 = list(self._graph.predecessors(node))[1]
        #             if self._graph.nodes[n0]["value"] is not None and self._graph.nodes[n1]["value"] is not None:
        #                 if self._graph.nodes[node]["function"] == "AND":
        #                     self._graph.nodes[node]["value"] = self._graph.nodes[n0]["value"] & self._graph.nodes[n1]["value"]
        #                 elif self._graph.nodes[node]["function"] == "OR":
        #                     self._graph.nodes[node]["value"] = self._graph.nodes[n0]["value"] | self._graph.nodes[n1]["value"]
        #                 elif self._graph.nodes[node]["function"] == "NOT":
        #                     self._graph.nodes[node]["value"] = ~self._graph.nodes[n1]["value"]
        #                 else:
        #                     print("Unknown function")
        return 0

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
