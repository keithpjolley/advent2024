#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import os
import sys
from itertools import groupby

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
        self._graph = self._create_graph()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self) -> list[list[int]]:
        return [[c for c in row] for row in self._raw_data.strip().split("\n")]

    def _create_graph(self: Self) -> "networkx.classes.digraph.DiGraph":
        # Create an emtpy directed graph.
        graph = nx.Graph()
        # Create nodes.
        graph.add_nodes_from(
            (
                f"{plant_type}:{j},{i}",
                {"plant_type": plant_type, "x": i, "y": j},
            )
            for j, row in enumerate(self._data)
            for i, plant_type in enumerate(row)
        )
        # Create edges. This will create a subgraph of connected nodes for each plant type.
        for alpha in graph.nodes():
            alpha_edges = [
                n
                for n, v in graph.nodes(data=True)
                if v["plant_type"] == graph.nodes()[alpha]["plant_type"]
                and (
                    (
                        v["x"] == graph.nodes()[alpha]["x"] + 1
                        and v["y"] == graph.nodes()[alpha]["y"]
                    )
                    or (
                        v["x"] == graph.nodes()[alpha]["x"]
                        and v["y"] == graph.nodes()[alpha]["y"] + 1
                    )
                    or (
                        v["x"] == graph.nodes()[alpha]["x"] - 1
                        and v["y"] == graph.nodes()[alpha]["y"]
                    )
                    or (
                        v["x"] == graph.nodes()[alpha]["x"]
                        and v["y"] == graph.nodes()[alpha]["y"] - 1
                    )
                )
            ]
            graph.add_edges_from((alpha, beta) for beta in alpha_edges)
        return graph

    def _draw(self: Self) -> None:  # pragma: no cover
        # For plotting/debug. Not used in the solution.
        import matplotlib.cm as cmx
        import matplotlib.colors as colors
        import matplotlib.pyplot as plt

        pos = {
            n: (
                self._graph.nodes()[n]["x"] + 0.5,
                len(self._data) - self._graph.nodes()[n]["y"] + 0.5,
            )
            for n in self._graph.nodes()
        }
        labels = {
            n: self._graph.nodes()[n]["plant_type"]
            for n in self._graph.nodes()
        }
        plant_types = list(
            set(nx.get_node_attributes(self._graph, "plant_type").values())
        )
        c_norm = colors.Normalize(vmin=0, vmax=len(plant_types))
        scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=plt.get_cmap("Set1"))
        node_color = {
            node: scalar_map.to_rgba(
                plant_types.index(self._graph.nodes()[node]["plant_type"])
            )
            for node in self._graph.nodes()
        }
        nx.draw_networkx(
            self._graph,
            pos=pos,
            labels=labels,
            node_color=node_color.values(),
            with_labels=True,
        )
        plt.grid("on")
        plt.show()

    def _part1(self: Self) -> int:
        """! I thought this would be faster. :/"""
        return sum(
            (2 * len(subgraph.nodes()))
            * (2 * len(subgraph.nodes()) - len(subgraph.edges()))
            for subgraph in (
                self._graph.subgraph(c).copy()
                for c in nx.connected_components(self._graph)
            )
        )

    def _top_bottom(
        self: Self,
        y_min: int,
        y_max: int,
        x_min: int,
        x_max: int,
        xy_pairs: list[tuple[int, int]],
    ) -> list[bool]:
        sides = []
        for dx, dy in [(0, -1), (0, +1)]:
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    sides.append(
                        (x, y) in xy_pairs and (x + dx, y + dy) not in xy_pairs
                    )
                sides.append(False)
        return sides

    def _left_right(
        self: Self,
        y_min: int,
        y_max: int,
        x_min: int,
        x_max: int,
        xy_pairs: list[tuple[int, int]],
    ) -> list[bool]:
        sides = []
        for dx, dy in [(-1, 0), (1, 0)]:
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    sides.append(
                        (x, y) in xy_pairs and (x + dx, y + dy) not in xy_pairs
                    )
                sides.append(False)
        return sides

    def _part2(self: Self) -> int:
        def range_of(values: ValuesView[int]) -> list[int]:
            return [min(values), max(values)]

        total = 0
        for subgraph in (
            self._graph.subgraph(c).copy()
            for c in nx.connected_components(self._graph)
        ):
            # Get the boundries of the subgraph.
            x_vals = nx.get_node_attributes(subgraph, "x").values()
            y_vals = nx.get_node_attributes(subgraph, "y").values()
            x_min, x_max = range_of(x_vals)
            y_min, y_max = range_of(y_vals)
            xy_pairs = list(zip(x_vals, y_vals))
            sides = self._top_bottom(y_min, y_max, x_min, x_max, xy_pairs)
            sides += self._left_right(y_min, y_max, x_min, x_max, xy_pairs)
            sides = sum([k for k, _ in groupby(sides)])
            area = len(subgraph.nodes())
            total += area * sides
        return total


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
