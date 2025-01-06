#!/usr/bin/env python3

from typing import TYPE_CHECKING, Never, Self, ValuesView

if TYPE_CHECKING:
    import networkx.classes.digraph  # pragma: no cover

import heapq
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
        self._parse_data()
        self.p1 = self._part1()
        self.p2 = self._part2()

    def __str__(self: Self) -> str:
        """! This is what's printed if the class is printed.
        @return: The message to be printed.
        """
        message = f"part 1: {self.p1}\npart 2: {self.p2}"
        return message

    def _parse_data(self: Self):
        graph = nx.Graph()
        for j, row in enumerate(self._raw_data.split("\n")):
            for i, col in enumerate(row):
                if col != "#":
                    if col in ["S", "E"]:
                        graph.add_node(col, x=i, y=j)
                    else:
                        graph.add_node(f"{i}.{j}", x=i, y=j)
        nodes = {(d["x"], d["y"]): n for n, d in graph.nodes(data=True)}
        for k, v in nodes.items():
            x, y = k
            if (x + 1, y) in nodes:
                graph.add_edge(v, nodes[(x + 1, y)])
            if (x, y + 1) in nodes:
                graph.add_edge(v, nodes[(x, y + 1)])
        # Remove dead-end nodes. Not perfect but hopefully saves some
        # time later on.
        num_nodes = -1
        while num_nodes != len(graph.nodes):
            num_nodes = len(graph.nodes)
            for node in list(graph.nodes):
                if (
                    node not in ["S", "E"]
                    and len(neighbors := list(graph.neighbors(node))) < 2
                ):
                    if len(neighbors) > 0:
                        graph.remove_edge(node, neighbors[0])
                    graph.remove_node(node)
        # Return adjacency list with weights all set to 1.
        self._graph = graph
        self._adj_list = {
            k: {kk: 1 for kk in v.keys()}
            for k, v in dict(graph.adjacency()).items()
        }

    def _draw_graph(self: Self):
        import matplotlib.pyplot as plt

        pos = {n: (d["x"], -d["y"]) for n, d in self._graph.nodes(data=True)}
        colors = [
            (
                "red"
                if n in ["S", "E"]
                else "green" if n in self._distances else "blue"
            )
            for n in self._graph.nodes
        ]
        nx.draw(self._graph, pos, node_color=colors, labels=self._distances)
        plt.show()

    def _dijkstra(self):
        # Adapted from: https://datagy.io/dijkstras-algorithm-python/
        start = "S"
        distances = {node: float("inf") for node in self._adj_list}
        distances[start] = 0

        # Priority queue to track nodes and current shortest distance.
        # (distance, node, direction)
        # "direction" starts at 1, the index of E in [N, E, S, W].
        priority_queue = [
            (0, start, 1),
        ]

        while priority_queue:
            # Pop the node with the smallest distance from the priority queue
            current_distance, current_node, current_direction = heapq.heappop(
                priority_queue
            )

            # Skip if a shorter distance to current_node is already found
            if current_distance > distances[current_node]:
                continue

            # Explore neighbors and update distances if a shorter path is found
            for neighbor, weight in self._adj_list[current_node].items():
                current_x, current_y = (
                    self._graph.nodes[current_node]["x"],
                    self._graph.nodes[current_node]["y"],
                )
                neighbor_x, neighbor_y = (
                    self._graph.nodes[neighbor]["x"],
                    self._graph.nodes[neighbor]["y"],
                )
                direction = [
                    current_y < neighbor_y,
                    current_x < neighbor_x,
                    current_y > neighbor_y,
                    current_x > neighbor_x,
                ].index(True)
                weight = 1 if direction == current_direction else 1001
                distance = current_distance + weight

                # If shorter path to neighbor is found, update distance and push to queue
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(
                        priority_queue, (distance, neighbor, direction)
                    )
        self._distances = distances

    def _part1(self: Self) -> int:
        self._dijkstra()
        self._draw_graph()
        return self._distances["E"]

    def _part2(self: Self) -> int:
        return 0


if __name__ == "__main__":  # pragma: no cover
    print(Day(sys.argv[1:]))

# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4 syntax=python
