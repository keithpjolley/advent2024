#!/usr/bin/env python3

import os
import sys

import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common import GetRawData


class Day:

    def __init__(self, args):
        self._get_raw = GetRawData(
            args, day=os.path.splitext(os.path.basename(__file__))[0]
        )
        self._raw_data = self._get_raw.raw_data.strip()
        self._data = self._parse_data()
        self._graph = self._create_graph()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self):
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self):
        return [
            [int(c) for c in row] for row in self._raw_data.strip().split("\n")
        ]

    def _create_graph(self):
        # Create an emtpy directed graph.
        graph = nx.DiGraph()
        # Create nodes.
        graph.add_nodes_from(
            (".".join([f"{j}", f"{i}", f"{c}"]), {"height": c, "i": i, "j": j})
            for j, r in enumerate(self._data)
            for i, c in enumerate(r)
        )
        # Create edges.
        for alpha in graph.nodes():
            alpha_edges = [
                n
                for n, v in graph.nodes(data=True)
                if v["height"] == graph.nodes()[alpha]["height"] + 1
                and (
                    (
                        v["i"] == graph.nodes()[alpha]["i"] + 1
                        and v["j"] == graph.nodes()[alpha]["j"]
                    )
                    or (
                        v["i"] == graph.nodes()[alpha]["i"]
                        and v["j"] == graph.nodes()[alpha]["j"] + 1
                    )
                    or (
                        v["i"] == graph.nodes()[alpha]["i"] - 1
                        and v["j"] == graph.nodes()[alpha]["j"]
                    )
                    or (
                        v["i"] == graph.nodes()[alpha]["i"]
                        and v["j"] == graph.nodes()[alpha]["j"] - 1
                    )
                )
            ]
            graph.add_edges_from((alpha, beta) for beta in alpha_edges)
        return graph

    def _part1(self):
        return sum(
            1
            for th in [
                n for n, v in self._graph.nodes(data=True) if v["height"] == 0
            ]
            for tt in [
                n for n, v in self._graph.nodes(data=True) if v["height"] == 9
            ]
            if nx.has_path(self._graph, th, tt)
        )

    def _part2(self):
        def paths(source, target):
            try:
                return len(
                    list(nx.all_shortest_paths(self._graph, source, target))
                )
            except nx.NetworkXNoPath:
                return 0

        return sum(
            paths(th, tt)
            for th in [
                n for n, v in self._graph.nodes(data=True) if v["height"] == 0
            ]
            for tt in [
                n for n, v in self._graph.nodes(data=True) if v["height"] == 9
            ]
        )


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
