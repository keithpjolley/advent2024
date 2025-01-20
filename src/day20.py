#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys

import matplotlib.pyplot as plt
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.common import GetRawData


class Day:

    def __init__(self: Self, args: list[Never]) -> None:
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._savings_threshold = (
            50 if "input" in args and "test" in args.input else 100
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._graph = self._parse_data()
        self._start = [
            n
            for n, v in self._graph.nodes(data=True)
            if v["node_type"] == "start"
        ][0]
        self._end = [
            n
            for n, v in self._graph.nodes(data=True)
            if v["node_type"] == "end"
        ][0]
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _draw(
        self: Self, graph=None, title=None, saveto=None
    ) -> None:  # pragma: no cover
        if saveto is None:
            plt.figure()
            plt.clf()
        if title is not None:
            plt.title(title)
        if graph is None:
            graph = self._graph
        try:
            labels = dict()
            for i, n in enumerate(
                nx.shortest_path(graph, self._start, self._end)
            ):
                if n not in [self._start, self._end]:
                    graph.nodes[n]["color"] = "b"
                labels[n] = i
        except (AttributeError, nx.NetworkXNoPath):
            labels = {n: n for n in graph.nodes()}
            pass
        w = max(n[0] for n in graph.nodes()) + 2
        h = max(n[1] for n in graph.nodes()) + 2
        for x in range(w):
            for y in range(h):
                if (x, y) not in graph.nodes:
                    graph.add_node((x, y), color="y", node_type="wall")
        nx.draw(
            graph,
            font_size=8,
            labels=labels,
            node_color=[v["color"] for _, v in graph.nodes(data=True)],
            node_shape="s",
            node_size=100,
            pos={n: (n[0], -n[1]) for n in graph.nodes()},
            with_labels=True,
        )
        if saveto is None:
            plt.show()
        else:
            plt.figure(figsize=(6, 6))
            plt.savefig(saveto)

    def _parse_data(self: Self) -> list[list[int]]:
        graph = nx.Graph()
        for y, row in enumerate(self._raw_data.split("\n")):
            for x, col in enumerate(row):
                if col == ".":
                    graph.add_node((x, y), color="g", node_type="path")
                if col == "S":
                    graph.add_node((x, y), color="m", node_type="start")
                if col == "E":
                    graph.add_node((x, y), color="r", node_type="end")
        for node in graph.nodes:
            x, y = node
            if (x + 1, y) in graph.nodes:
                graph.add_edge(node, (x + 1, y))
            if (x, y + 1) in graph.nodes:
                graph.add_edge(node, (x, y + 1))
        return graph

    def _part1(self: Self) -> int:
        """! A better way would be to use the shortest path, label each
        node with its distance from the start and then look for the
        delta of nodes two straight steps apart.
        """
        savings = 0
        spl_nocheats = nx.shortest_path_length(
            self._graph, self._start, self._end
        )

        for col in range(1, max(n[1] for n in self._graph.nodes) + 1):
            for row in range(1, max(n[0] for n in self._graph.nodes) + 1):
                if (col, row) not in self._graph.nodes:
                    for j in [(0, 1), (1, 0)]:
                        if (
                            (col + j[0], row + j[1]) not in self._graph.nodes
                        ) or (
                            (col - j[0], row - j[1]) not in self._graph.nodes
                        ):
                            continue
                        graph = self._graph.copy()
                        graph.add_node(
                            (col, row), node_type="cheat", color="m"
                        )
                        graph.add_edge((col, row), (col + j[0], row + j[1]))
                        graph.add_edge((col, row), (col - j[0], row - j[1]))
                        if (
                            spl_nocheats
                            - nx.shortest_path_length(
                                graph, self._start, self._end
                            )
                        ) >= 100:
                            savings += 1
        return savings

    def _manhattan(
        self: Self, distance: int, start: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """! Return a list of coordinates that are at most `distance`
        steps away, and not at the starting point."""
        x, y = start
        return [
            (i + x, j + y)
            for i in range(-distance, distance + 1)
            for j in range(-distance, distance + 1)
            if (abs(i) + abs(j)) <= distance and (i, j) != (0, 0)
        ]

    def _part2(self: Self) -> int:
        shortest_path = nx.shortest_path(self._graph, self._start, self._end)
        nx.set_node_attributes(self._graph, None, "step")
        for i, n in enumerate(shortest_path):
            self._graph.nodes[n]["step"] = i
        savings = 0
        for n in shortest_path:
            for p in self._manhattan(20, n):
                if p in self._graph.nodes:
                    s1 = self._graph.nodes[p]["step"]
                    s2 = self._graph.nodes[n]["step"]
                    if s1 is not None and s2 is not None:
                        saving = (
                            s1 - s2 - (abs(p[0] - n[0]) + abs(p[1] - n[1]))
                        )
                        if saving >= self._savings_threshold:
                            savings += 1
        return savings


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
